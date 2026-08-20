import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

// 1. Importamos o nosso serviço recém-criado
import { CarrinhoService } from '../../services/carrinho';

@Component({
  selector: 'app-catalogo',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './catalogo.html',
  styleUrls: ['./catalogo.css']
})
export class Catalogo {
  produtos = [
    { id: 1, nome: 'Camiseta Básica Preta', preco: 49.90, imagem: 'https://via.placeholder.com/250' },
    { id: 2, nome: 'Vestido Florido', preco: 129.90, imagem: 'https://via.placeholder.com/250' },
    { id: 3, nome: 'Conjunto Moletom', preco: 199.90, imagem: 'https://via.placeholder.com/250' }
  ];

  // 2. Injetamos o serviço no construtor para o Angular liberar o acesso
  constructor(private carrinhoService: CarrinhoService) {}

  adicionarAoCarrinho(produto: any) {
    // 3. Enviamos o produto para a memória do serviço!
    this.carrinhoService.adicionarItem(produto);
    
    // Mantemos um alerta rápido só para o usuário saber que deu certo
    alert(`O produto ${produto.nome} foi adicionado ao carrinho!`);
  }
}