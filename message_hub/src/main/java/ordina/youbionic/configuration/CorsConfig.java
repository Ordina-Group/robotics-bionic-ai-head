package ordina.youbionic.configuration;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

@Configuration
public class CorsConfig {

    @Value("${cors.allowedOrigins}")
    private String allowedOrigins;


    @Bean
    public CorsFilter corsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();

        // Allow requests from any origin (you can specify specific origins if needed)
        config.addAllowedOrigin(allowedOrigins);

        config.setAllowCredentials(true);

        // Allow specific HTTP methods (e.g., GET, POST, PUT, DELETE)
        config.addAllowedMethod("*");

        // Allow specific headers (e.g., Authorization, Content-Type)
        config.addAllowedHeader("*");

        source.registerCorsConfiguration("/**", config);
        return new CorsFilter(source);
    }
}
