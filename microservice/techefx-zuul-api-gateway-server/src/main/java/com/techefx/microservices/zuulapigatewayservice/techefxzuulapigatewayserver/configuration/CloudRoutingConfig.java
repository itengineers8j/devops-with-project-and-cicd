package com.techefx.microservices.zuulapigatewayservice.techefxzuulapigatewayserver.configuration;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class CloudRoutingConfig {

    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
                //swagger documentation
                .route("ventes_docs", r ->r.path("/api/ventes/**")
                        .filters(f -> f.rewritePath("^/api/ventes", ""))
                        .uri("http://localhost:8500/"))
                .route("produits_service", r ->r.path("/api/produits/**")
                        .filters(f -> f.rewritePath("^/api/produits", ""))
                        .uri("http://localhost:8600/"))
                .route("clients_service", r ->r.path("/api/clients/**")
                        .filters(f -> f.rewritePath("^/api/clients", ""))
                        .uri("http://localhost:8900/"))

                //ressources
                .route("ventes_service", r ->r.path("/ventes/**")
                        .uri("http://localhost:8700/"))
                .route("produits_service", r ->r.path("/produits/**")
                        .uri("http://localhost:8700/"))
                .route("clients_service", r ->r.path("/clients/**")
                        .uri("http://localhost:8700/"))
                .route("commandes_service", r ->r.path("/commandes/**")
                        .uri("http://localhost:8700/"))
                .build();
    }

}

