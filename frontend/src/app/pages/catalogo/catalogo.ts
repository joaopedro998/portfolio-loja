import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ProdutoService } from '../../services/produto';

@Component({
  selector: 'app-catalogo',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './catalogo.html',
  styleUrls: ['./catalogo.css']
})
export class Catalogo implements OnInit {
  produtos: any[] = [];

  constructor(
    private produtoService: ProdutoService,
    // 1. Injetamos o atualizador de tela
    private cdr: ChangeDetectorRef 
  ) {}

  ngOnInit() {
    this.carregarProdutos();
  }

  carregarProdutos() {
    this.produtoService.obterProdutos().subscribe({
      next: (dadosDaApi) => {
        this.produtos = dadosDaApi;
        // 2. Avisamos o HTML: "Os dados chegaram, desenhe a tela agora!"
        this.cdr.detectChanges(); 
      },
      error: (erro) => {
        console.error('Ops! Erro ao buscar os produtos:', erro);
      }
    });
  }
}