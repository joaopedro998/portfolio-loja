import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CarrinhoService {
  
  private itens: any[] = [];

  constructor() { }

  adicionarItem(produto: any) {
    const itemExistente = this.itens.find(item => item.id === produto.id);
    
    if (itemExistente) {
      itemExistente.quantidade += 1;
    } else {
      this.itens.push({ ...produto, quantidade: 1 });
    }
  }

  obterItens() {
    return this.itens;
  }

  calcularTotal() {
    return this.itens.reduce((total, item) => total + (item.preco * item.quantidade), 0);
  }

  limparCarrinho() {
    this.itens = [];
  }
}