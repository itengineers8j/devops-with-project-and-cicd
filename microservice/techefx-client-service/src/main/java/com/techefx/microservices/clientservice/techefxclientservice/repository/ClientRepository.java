package com.techefx.microservices.clientservice.techefxclientservice.repository;

import com.techefx.microservices.clientservice.techefxclientservice.models.Client;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ClientRepository extends JpaRepository<Client, Integer> {
}
