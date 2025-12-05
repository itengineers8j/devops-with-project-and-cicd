package com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.controller;

import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.beans.Client;
import com.techefx.microservices.productenquiryservice.techefxproductenquiryservice.client.ClientClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/clients")
public class ClientController {

    @Autowired
    private ClientClient clientClient;

    @PostMapping(value = "/create")
    public ResponseEntity<Client> saveClient(@RequestBody Client client){
        return clientClient.saveClient(client);
    }

    @GetMapping(value = "/all")
    public List<Client> getAllclients (){
        return clientClient.getAllClients();
    }

    @GetMapping(value = "/{id}")
    public ResponseEntity<Client> getClientById(@PathVariable int id){

        ResponseEntity<Client> getClient = clientClient.getClientById(id);

        if(getClient.getStatusCodeValue() == 200){
            return new ResponseEntity<>(getClient.getBody(), HttpStatus.OK);
        } else if (getClient.getStatusCodeValue() == 404) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        } else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }


}
