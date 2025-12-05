package com.techefx.microservices.productstockservice.techefxproductstockservice.controller;

import com.techefx.microservices.productstockservice.techefxproductstockservice.beans.ProductStockBean;
import com.techefx.microservices.productstockservice.techefxproductstockservice.entity.ProductStock;
import com.techefx.microservices.productstockservice.techefxproductstockservice.repository.ProductStockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class ProductStockController {

    @Autowired
    Environment environment;
    @Autowired
    ProductStockRepository productStockRepository;

    @GetMapping("/checkProduct/{productName}/{productAvailability}")
    public ProductStockBean checkProductStock(@PathVariable String productName, @PathVariable String productAvailability){

        ProductStock productStock = productStockRepository.findByProductNameAndProductAvailability(productName, productAvailability);

        ProductStockBean productStockBean = new ProductStockBean(
                productStock.getId(),
                productStock.getProductName(),
                productStock.getProductPrice(),
                productStock.getProductAvailability(),
                productStock.getDiscountOffer(),
                Integer.parseInt(environment.getProperty("local.server.port"))
        );

        return productStockBean;
    }


}
