import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CarrinhoService } from '../../services/carrinho';

@Component({
  selector: 'app-carrinho',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './carrinho.html',
  styleUrls: ['./carrinho.css']
})
export class Carrinho implements OnInit {
  itensCarrinho: any[] = [];
  total: number = 0;

  // Substitua pelo número real das donas depois (com DDI e DDD, ex: 5535999999999)
  numeroWhatsApp = '5535900000000'; 

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

    // 1. Monta o texto do pedido
    let texto = `Olá! Gostaria de finalizar um pedido.%0A%0A`;
    texto += `*Resumo da Compra:*%0A`;
    
    this.itensCarrinho.forEach(item => {
      texto += `- ${item.quantidade}x ${item.nome} (R$ ${item.preco.toFixed(2)})%0A`;
    });

    texto += `%0A*Total: R$ ${this.total.toFixed(2)}*`;

    // 2. Cria o link oficial do WhatsApp
    const linkWhatsApp = `https://wa.me/${this.numeroWhatsApp}?text=${texto}`;

    // 3. Abre o link em uma nova aba
    window.open(linkWhatsApp, '_blank');

    // 4. Limpa o carrinho após fechar o pedido
    this.carrinhoService.limparCarrinho();
    this.atualizarCarrinho();
  }
}