package com.techefx.microservices.produitservice.techefxproduitservice;

import com.techefx.microservices.produitservice.techefxproduitservice.models.Produits;
import com.techefx.microservices.produitservice.techefxproduitservice.service.ProduitService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@SpringBootApplication
@EnableSwagger2
public class TechefxProduitServiceApplication implements CommandLineRunner {

	@Autowired
	private ProduitService produitService;

	public static void main(String[] args) {
		SpringApplication.run(TechefxProduitServiceApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {

		Produits produits = new Produits(1, "Chaussure", "chaussure homme", 20000);
		Produits produits1 = new Produits(2, "Chemise", "chaussure homme", 8000);

		produitService.addProduct(produits);
		produitService.addProduct(produits1);
	}
}
