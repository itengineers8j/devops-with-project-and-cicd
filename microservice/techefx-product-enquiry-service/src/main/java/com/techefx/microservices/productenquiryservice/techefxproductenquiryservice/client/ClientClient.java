package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.client;

import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.Client;
import org.springframework.cloud.loadbalancer.annotation.LoadBalancerClient;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;

@FeignClient(name = "techefx-client-service")
@LoadBalancerClient(name = "techefx-client-service")
public interface ClientClient {

    @PostMapping(value = "/clients/create")
    public ResponseEntity<Client> saveClient(@RequestBody Client client);

    @GetMapping(value = "/clients/all")
    public List<Client> getAllClients ();

    @GetMapping(value = "/clients/{id}")
    public ResponseEntity<Client> getClientById(@PathVariable int id);

}
