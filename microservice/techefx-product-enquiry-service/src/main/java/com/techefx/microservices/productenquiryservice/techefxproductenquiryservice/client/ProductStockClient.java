package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.client;

import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.ProductEnquiryBean;
import org.springframework.cloud.loadbalancer.annotation.LoadBalancerClient;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "techefx-product-stock-service")
@LoadBalancerClient(name = "echefx-product-stock-service")
public interface ProductStockClient {

    @GetMapping("/checkProduct/{productName}/{productAvailability}")
    public ProductEnquiryBean checkProductStock(@PathVariable String productName, @PathVariable String productAvailability);
}
