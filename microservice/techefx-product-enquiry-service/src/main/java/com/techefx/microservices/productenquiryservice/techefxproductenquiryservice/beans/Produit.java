package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Produit {

    private int id;

    private String nom;

    private String description;

    private int prix;
}
