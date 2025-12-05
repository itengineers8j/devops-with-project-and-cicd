package com.techefx.microservices.produitservice.techefxproduitservice.controller;

import com.techefx.microservices.produitservice.techefxproduitservice.models.Produits;
import com.techefx.microservices.produitservice.techefxproduitservice.service.ProduitService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/produits")
public class ProduitController {

    @Autowired
    private ProduitService produitService;

    @PostMapping(value = "/create", produces = MediaType.APPLICATION_JSON_VALUE, consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Produits> saveProduits(@RequestBody Produits produits){
        Produits newProduits = produitService.addProduct(produits);

        if(newProduits != null){
            return new ResponseEntity<>(newProduits, HttpStatus.CREATED);
        }else{
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
    }

    @GetMapping(value = "/all", produces = MediaType.APPLICATION_JSON_VALUE)
    public List<Produits> getAllProducts (){
        return produitService.getAllProducts();
    }

    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Produits> getProduitsById(@PathVariable int id){
        Optional<Produits> getProduits = produitService.getProductById(id);

        if(getProduits.isPresent()){
            return new ResponseEntity<>(getProduits.get(), HttpStatus.OK);
        }else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

    }

}
