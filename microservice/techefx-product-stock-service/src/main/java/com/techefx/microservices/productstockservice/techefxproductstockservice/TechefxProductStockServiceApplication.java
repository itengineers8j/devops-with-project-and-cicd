package com.techefx.microservices.productstockservice.techefxproductstockservice;

import com.techefx.microservices.productstockservice.techefxproductstockservice.entity.ProductStock;
import com.techefx.microservices.productstockservice.techefxproductstockservice.repository.ProductStockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
//import springfox.documentation.swagger2.annotations.EnableSwagger2;

@SpringBootApplication
//@EnableSwagger2
public class TechefxProductStockServiceApplication implements CommandLineRunner {

	@Autowired
	ProductStockRepository productStockRepository;

	public static void main(String[] args) {
		SpringApplication.run(TechefxProductStockServiceApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {

		ProductStock productStock = new ProductStock(1, "bat",5000,"yes",20 );
		ProductStock productStock1 = new ProductStock(2, "ball",500,"yes",40 );
		ProductStock productStock2 = new ProductStock(3, "helmet",3000,"yes",20 );
		ProductStock productStock3 = new ProductStock(4, "bat2",5000,"yes",10 );

		productStockRepository.save(productStock);
		productStockRepository.save(productStock1);
		productStockRepository.save(productStock2);
		productStockRepository.save(productStock3);

	}

}
