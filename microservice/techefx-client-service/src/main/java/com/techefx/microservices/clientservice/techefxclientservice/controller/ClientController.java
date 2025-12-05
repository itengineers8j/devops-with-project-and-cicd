package com.techefx.microservices.clientservice.techefxclientservice.controller;

import com.techefx.microservices.clientservice.techefxclientservice.models.Client;
import com.techefx.microservices.clientservice.techefxclientservice.service.ClientService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/clients")
public class ClientController {

    @Autowired
    private ClientService clientService;

    @PostMapping(value = "/create", produces = MediaType.APPLICATION_JSON_VALUE, consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Client> saveClient(@RequestBody Client client){
        Client newClient = clientService.addClient(client);

        if(newClient != null){
            return new ResponseEntity<>(newClient, HttpStatus.CREATED);
        }else{
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
    }

    @GetMapping(value = "/all", produces = MediaType.APPLICATION_JSON_VALUE)
    public List<Client> getAllClients (){
        return clientService.getAllClient();
    }

    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Client> getClientById(@PathVariable int id){
        Optional<Client> getClient = clientService.getClientById(id);

        if(getClient.isPresent()){
            return new ResponseEntity<>(getClient.get(), HttpStatus.OK);
        }else{
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

    }

}
