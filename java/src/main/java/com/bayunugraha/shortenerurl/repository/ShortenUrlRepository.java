package com.bayunugraha.shortenerurl.repository;

import com.bayunugraha.shortenerurl.model.ShortenUrl;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ShortenUrlRepository extends JpaRepository<ShortenUrl, String> {
}
