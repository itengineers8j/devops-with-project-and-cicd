package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@SpringBootApplication
@EnableFeignClients("com.techefx.microservices.productenquiryservice.techefxproductenquiryservice")
@EnableSwagger2
public class TechefxProductEnquiryServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(TechefxProductEnquiryServiceApplication.class, args);
	}

}
