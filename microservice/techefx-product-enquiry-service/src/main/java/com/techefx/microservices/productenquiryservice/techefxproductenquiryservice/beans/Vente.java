package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Vente {

    private int id;

    private int quantite;

    private int prixTotal;

    private int idClient;

    private int idProduit;

}
