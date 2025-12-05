package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.controller;

import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.Client;
import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.Commande;
import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.Produit;
import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.Vente;
import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.client.ClientClient;
import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.client.ProduitClient;
import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.client.VenteClient;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/commandes")
public class CommandeController {

    @Autowired
    private ClientClient clientClient;

    @Autowired
    private ProduitClient produitClient;

    @Autowired
    private VenteClient venteClient;

    @GetMapping("/client/{clientId}")
    private Commande getCommande(@PathVariable int clientId){

        Client client = clientClient.getClientById(clientId).getBody();
        Vente vente = venteClient.getVenteByClientId(client.getId()).getBody();
        Produit produit = produitClient.getProduitsById(vente.getIdProduit()).getBody();

        return new Commande(
            client.getNom(),
            produit.getNom(),
            vente.getQuantite(),
            produit.getPrix(),
        vente.getQuantite()*produit.getPrix()
        );
    }
}
