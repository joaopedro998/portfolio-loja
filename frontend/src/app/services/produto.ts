import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProdutoService {
  
  // O endereço base do nosso servidor Flask!
  private apiUrl = 'http://127.0.0.1:5000/api/produtos';

  // Injetamos o "telefone" do Angular (HttpClient)
  constructor(private http: HttpClient) {}

  // 1. Busca TODOS os produtos (Usado pelo Catalogo / Vitrine)
  obterProdutos(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  // 2. Busca APENAS UM produto pelo ID (Usado pelo ProdutoDetalhe)
  obterProdutoPorId(id: number): Observable<any> {
    // Faz uma requisição GET para http://127.0.0.1:5000/api/produtos/1
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }
}