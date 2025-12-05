package com.techefx.microservices.venteservice.techefxventeservice;

import com.techefx.microservices.venteservice.techefxventeservice.models.Vente;
import com.techefx.microservices.venteservice.techefxventeservice.service.VenteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@SpringBootApplication
@EnableSwagger2
public class TechefxVenteServiceApplication implements CommandLineRunner {

	@Autowired
	private VenteService venteService;

	public static void main(String[] args) {
		SpringApplication.run(TechefxVenteServiceApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {

		Vente vente = new Vente(1, 2,40000, 1,1);

		Vente vente1 = new Vente(2, 1,8000, 2,2);

		venteService.addVente(vente);
		venteService.addVente(vente1);
	}
}
