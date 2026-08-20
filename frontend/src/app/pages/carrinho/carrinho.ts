import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
// 1. Importamos o FormsModule para conseguir ler as caixinhas de seleção
import { FormsModule } from '@angular/forms'; 
import { CarrinhoService } from '../../services/carrinho';

@Component({
  selector: 'app-carrinho',
  standalone: true,
  // 2. Adicionamos o FormsModule aqui nos imports
  imports: [CommonModule, RouterModule, FormsModule], 
  templateUrl: './carrinho.html',
  styleUrls: ['./carrinho.css']
})
export class Carrinho implements OnInit {
  itensCarrinho: any[] = [];
  total: number = 0;
  numeroWhatsApp = '5535900000000'; 

  // Variáveis para guardar as escolhas do cliente
  formaPagamento: string = '';
  tipoEntrega: string = '';

  constructor(private carrinhoService: CarrinhoService) {}

  ngOnInit() {
    this.atualizarCarrinho();
  }

  atualizarCarrinho() {
    this.itensCarrinho = this.carrinhoService.obterItens();
    this.total = this.carrinhoService.calcularTotal();
  }

  finalizarPedido() {
    if (this.itensCarrinho.length === 0) {
      alert('Seu carrinho está vazio!');
      return;
    }

    // 3. Validação: obriga o cliente a escolher as opções antes de ir pro WhatsApp
    if (!this.formaPagamento || !this.tipoEntrega) {
      alert('Por favor, selecione o tipo de entrega e a forma de pagamento para continuar.');
      return;
    }

    let texto = `Olá! Gostaria de finalizar um pedido.%0A%0A`;
    texto += `*Resumo da Compra:*%0A`;
    
    this.itensCarrinho.forEach(item => {
      texto += `- ${item.quantidade}x ${item.nome} (R$ ${item.preco.toFixed(2)})%0A`;
    });

    texto += `%0A*Total: R$ ${this.total.toFixed(2)}*%0A%0A`;
    
    // 4. Adiciona as escolhas no texto da mensagem
    texto += `*Entrega:* ${this.tipoEntrega}%0A`;
    texto += `*Pagamento:* ${this.formaPagamento}`;

    const linkWhatsApp = `https://wa.me/${this.numeroWhatsApp}?text=${texto}`;
    window.open(linkWhatsApp, '_blank');

    this.carrinhoService.limparCarrinho();
    this.atualizarCarrinho();
  }
}