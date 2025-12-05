package com.techefx.microservices.produitservice.techefxproduitservice.service;

import com.techefx.microservices.produitservice.techefxproduitservice.models.Produits;
import com.techefx.microservices.produitservice.techefxproduitservice.repository.ProduitRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ProduitService {

    @Autowired
    private ProduitRepository produitRepository;

    public List<Produits> getAllProducts(){
        return produitRepository.findAll();
    }

    public Optional<Produits> getProductById(int id){
        return produitRepository.findById(id);
    }

    public Produits addProduct(Produits produit){
        return produitRepository.save(produit);
    }
}
