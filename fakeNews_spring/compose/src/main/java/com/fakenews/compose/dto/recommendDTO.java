package com.fakenews.compose.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class recommendDTO {

    private String title;
    private String link;
    private String description;

}
