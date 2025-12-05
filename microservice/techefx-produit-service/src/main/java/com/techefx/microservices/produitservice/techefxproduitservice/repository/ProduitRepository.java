package com.techefx.microservices.produitservice.techefxproduitservice.repository;

import com.techefx.microservices.produitservice.techefxproduitservice.models.Produits;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProduitRepository extends JpaRepository<Produits, Integer> {

}
