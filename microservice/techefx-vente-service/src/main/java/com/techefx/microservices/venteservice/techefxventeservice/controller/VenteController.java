package com.techefx.microservices.venteservice.techefxventeservice.controller;

import com.techefx.microservices.venteservice.techefxventeservice.models.Vente;
import com.techefx.microservices.venteservice.techefxventeservice.service.VenteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/ventes")
public class VenteController {

    @Autowired
    private VenteService venteService;

    @PostMapping(value = "/create", produces = MediaType.APPLICATION_JSON_VALUE, consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Vente> saveVente(@RequestBody Vente vente){
        Vente newVente = venteService.addVente(vente);

        if(newVente != null){
            return new ResponseEntity<>(newVente, HttpStatus.CREATED);
        }else{
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
    }

    @GetMapping(value = "/all", produces = MediaType.APPLICATION_JSON_VALUE)
    public List<Vente> getAllVentes (){
        return venteService.getAllVente();
    }

    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Vente> getVenteById(@PathVariable int id){
        Optional<Vente> getVente = venteService.getVenteById(id);

        if(getVente.isPresent()){
            return new ResponseEntity<>(getVente.get(), HttpStatus.OK);
        }else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

    }

    @GetMapping(value = "/client/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Vente> getVenteByClientId(@PathVariable int id){
        Optional<Vente> getVente = venteService.getVenteByIdClient(id);

        if(getVente.isPresent()){
            return new ResponseEntity<>(getVente.get(), HttpStatus.OK);
        }else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

    }
}
