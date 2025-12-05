package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.controller;

import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.Produit;
import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.client.ProduitClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@RestController
@RequestMapping("/produits")
public class ProduitController {

    @Autowired
    private ProduitClient produitClient;

    @PostMapping(value = "/create")
    public ResponseEntity<Produit> saveProduits(@RequestBody Produit produit){
        return produitClient.saveProduits(produit);
    }

    @GetMapping(value = "/all")
    public List<Produit> getAllProducts (){
        return produitClient.getAllProducts();
    }

    @GetMapping(value = "/{id}")
    public ResponseEntity<Produit> getProduitsById(@PathVariable int id){

        ResponseEntity<Produit> getProduits = produitClient.getProduitsById(id);
        System.out.println(getProduits.getStatusCodeValue());
        if(getProduits.getStatusCodeValue() == 200){
            return new ResponseEntity<>(getProduits.getBody(), HttpStatus.OK);
        } else if (getProduits.getStatusCodeValue() == 404) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        } else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}
