package com.techefx.microservices.clientservice.techefxclientservice.service;

import com.techefx.microservices.clientservice.techefxclientservice.models.Client;
import com.techefx.microservices.clientservice.techefxclientservice.repository.ClientRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ClientService {

    @Autowired
    private ClientRepository clientRepository;

    public List<Client> getAllClient(){
        return clientRepository.findAll();
    }

    public Optional<Client> getClientById(int id){
        return clientRepository.findById(id);
    }

    public Client addClient(Client client){
        return clientRepository.save(client);
    }
}
