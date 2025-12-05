package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.client;

import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.Vente;
import org.springframework.cloud.loadbalancer.annotation.LoadBalancerClient;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;

@FeignClient(name = "techefx-vente-service")
@LoadBalancerClient(name = "techefx-vente-service")
public interface VenteClient {

    @PostMapping(value = "ventes/create")
    public ResponseEntity<Vente> saveVente(@RequestBody Vente vente);

    @GetMapping(value = "ventes/all")
    public List<Vente> getAllVentes ();

    @GetMapping(value = "ventes/{id}")
    public ResponseEntity<Vente> getVenteById(@PathVariable int id);

    @GetMapping(value = "ventes/client/{id}")
    public ResponseEntity<Vente> getVenteByClientId(@PathVariable int id);

}

