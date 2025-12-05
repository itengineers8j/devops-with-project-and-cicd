package com.techefx.microservices.venteservice.techefxventeservice.service;

import ch.qos.logback.core.net.server.Client;
import com.techefx.microservices.venteservice.techefxventeservice.models.Vente;
import com.techefx.microservices.venteservice.techefxventeservice.repository.VenteRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class VenteService {

    @Autowired
    private VenteRepository venteRepository;

    public List<Vente> getAllVente(){
        return venteRepository.findAll();
    }

    public Optional<Vente> getVenteById(int id){
        return venteRepository.findById(id);
    }

    public Vente addVente(Vente vente){
        return venteRepository.save(vente);
    }

    public Optional<Vente> getVenteByIdClient(int idClient){
        return venteRepository.findByIdClient(idClient);
    }

}
