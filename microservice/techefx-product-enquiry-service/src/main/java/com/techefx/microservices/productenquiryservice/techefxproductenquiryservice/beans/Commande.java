package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Commande {

    private String clientName;

    private String produitName;

    private int produitQuantite;

    private int unitPrice;

    private double total;
}
