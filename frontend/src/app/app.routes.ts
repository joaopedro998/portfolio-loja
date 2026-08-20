import { Routes } from '@angular/router';
import { Catalogo } from './pages/catalogo/catalogo';
import { Carrinho } from './pages/carrinho/carrinho';
import { ProdutoDetalhe } from './pages/produto-detalhe/produto-detalhe';

export const routes: Routes = [
  { path: '', component: Catalogo },
  { path: 'carrinho', component: Carrinho },
  // 2. Criamos a rota com um parâmetro dinâmico chamado "id"
  { path: 'produto/:id', component: ProdutoDetalhe } 
];