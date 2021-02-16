package com.bayunugraha.shortenerurl.model;

import lombok.*;

import javax.persistence.*;

@Entity
@Table()
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ShortenUrl {

    @Id
    @Column(name="id")
    private String id;

    @Column(name="originalURL", nullable = false)
    private String originalURL;
}
