import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { ProdutoService } from '../../services/produto';
import { CarrinhoService } from '../../services/carrinho';

@Component({
  selector: 'app-produto-detalhe',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './produto-detalhe.html',
  styleUrls: ['./produto-detalhe.css']
})
export class ProdutoDetalhe implements OnInit {
  // A variável começa vazia até o back-end responder
  produto: any; 
  tamanhoSelecionado: string = '';

  constructor(
    private route: ActivatedRoute,
    private produtoService: ProdutoService,
    private carrinhoService: CarrinhoService, // <-- VÍRGULA ADICIONADA AQUI
    private cdr: ChangeDetectorRef            // <-- AGORA ELE VAI FUNCIONAR
  ) {}

  ngOnInit() {
    // RADAR 1: Verifica se o Angular conseguiu ler o número na URL
    const idStr = this.route.snapshot.paramMap.get('id');
    console.log('RADAR 1 - ID lido da URL:', idStr);
    
    const id = Number(idStr);
    console.log('RADAR 2 - Convertido para número. Vou chamar a API para o ID:', id);
    
    // Liga para o Flask
    this.produtoService.obterProdutoPorId(id).subscribe({
      next: (dadosDaApi) => {
        // RADAR 3: Verifica se a resposta realmente chegou aqui dentro
        console.log('RADAR 3 - Resposta do Python chegou!', dadosDaApi);
        
        this.produto = dadosDaApi;
        this.cdr.detectChanges(); 
      },
      error: (erro) => {
        console.error('RADAR 3 - Deu erro na chamada:', erro);
      }
    });
  }

  selecionarTamanho(tamanho: string) {
    this.tamanhoSelecionado = tamanho;
  }

  adicionarAoCarrinho() {
    if (!this.tamanhoSelecionado) {
      return;
    }
    
    // Adiciona o produto no carrinho junto com o tamanho escolhido
    const itemParaCarrinho = {
      ...this.produto,
      tamanho: this.tamanhoSelecionado
    };
    
    this.carrinhoService.adicionarItem(itemParaCarrinho);
    alert('Peça adicionada ao carrinho com sucesso! 🛍️');
  }
}