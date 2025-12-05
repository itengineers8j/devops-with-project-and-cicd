package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.controller;

import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.Vente;
import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.client.VenteClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/ventes")
public class VenteController {

    @Autowired
    private VenteClient venteClient;

    @PostMapping(value = "/create")
    public ResponseEntity<Vente> saveVente(@RequestBody Vente vente){
        return venteClient.saveVente(vente);
    }

    @GetMapping(value = "/all")
    public List<Vente> getAlventes (){
        return venteClient.getAllVentes();
    }

    @GetMapping(value = "/{id}")
    public ResponseEntity<Vente> getVenteById(@PathVariable int id){

        ResponseEntity<Vente> getVente = venteClient.getVenteById(id);

        if(getVente.getStatusCodeValue() == 200){
            return new ResponseEntity<>(getVente.getBody(), HttpStatus.OK);
        } else if (getVente.getStatusCodeValue() == 404) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        } else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}
