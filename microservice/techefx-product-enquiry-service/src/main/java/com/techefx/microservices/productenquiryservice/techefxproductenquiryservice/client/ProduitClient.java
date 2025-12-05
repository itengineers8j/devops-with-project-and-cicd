package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.client;

import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.Produit;
import org.springframework.cloud.loadbalancer.annotation.LoadBalancerClient;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@FeignClient(name = "techefx-produit-service")
@LoadBalancerClient(name = "techefx-produit-service")
public interface ProduitClient {

    @PostMapping(value = "/produits/create")
    public ResponseEntity<Produit> saveProduits(@RequestBody Produit produits);

    @GetMapping(value = "/produits/all")
    public List<Produit> getAllProducts ();

    @GetMapping(value = "/produits/{id}")
    public ResponseEntity<Produit> getProduitsById(@PathVariable int id);

}

