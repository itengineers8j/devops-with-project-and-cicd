package com.techefx.microservices.productstockservice.techefxproductstockservice.repository;

import com.techefx.microservices.productstockservice.techefxproductstockservice.entity.ProductStock;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductStockRepository extends JpaRepository<ProductStock, Integer> {

    ProductStock findByProductNameAndProductAvailability(String productName, String productAvailability);

}
