package com.techefx.microservices.clientservice.techefxclientservice;

import com.techefx.microservices.clientservice.techefxclientservice.models.Client;
import com.techefx.microservices.clientservice.techefxclientservice.service.ClientService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@SpringBootApplication
@EnableSwagger2
public class TechefxClientServiceApplication implements CommandLineRunner {

	@Autowired
	private ClientService clientService;

	public static void main(String[] args) {
		SpringApplication.run(TechefxClientServiceApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {

		Client client = new Client(1, "donfack", "kemane");
		Client client1 = new Client(2, "nafack", "ivan");

		clientService.addClient(client);
		clientService.addClient(client1);
	}
}
