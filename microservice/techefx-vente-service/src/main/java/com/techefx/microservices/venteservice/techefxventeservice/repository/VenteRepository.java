package com.techefx.microservices.venteservice.techefxventeservice.repository;

import com.techefx.microservices.venteservice.techefxventeservice.models.Vente;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface VenteRepository extends JpaRepository<Vente, Integer> {

    public Optional<Vente> findByIdClient(int idClient);
}
