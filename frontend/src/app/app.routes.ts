import { Routes } from '@angular/router';
import { Catalogo } from './pages/catalogo/catalogo';
import { Carrinho } from './pages/carrinho/carrinho';

export const routes: Routes = [
  { path: '', component: Catalogo },
  { path: 'carrinho', component: Carrinho }
];