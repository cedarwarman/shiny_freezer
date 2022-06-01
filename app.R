library(shiny)
library(lubridate)
library(googlesheets4)
library(ggplot2)
library(plotly)

# Functions ---------------------------------------------------------------
import_dataset <- function(sheet_id) {
  # Avoiding permissions (make sure sheet is public)
  gs4_deauth()
  df <- read_sheet(sheet_id)
  
  # Making a single column for date and time
  df$date_time <- ymd_hms(paste(df$date, df$time))
  # Changing the data column from a string to date type
  df$date <- ymd(df$date)
  
  return(df)
}

# This function will make a temperature plot
make_temp_plot <- function(input_df) {
  output_plot <- ggplotly(input_df %>%
    ggplot(aes(date_time, as.numeric(temp_c),
      # group = 1, # Supposedly necessary in some cases
      text = paste0("Date and Time: <b>", date_time, "</b>",
                    "<br>Temperature: <b>", temp_c, " ºC</b>"))) +
    # geom_smooth(method = "loess", se = FALSE, span = 0.01, color = "white", size = 0.5) +
    geom_point(size = 2, shape = 16, alpha = 1, color = "blue") +
    geom_hline(yintercept = -65, size = 1, linetype = "dashed", color = "orange") +
    scale_y_continuous(breaks = seq(-90, 0, 10),
                       labels = seq(-90, 0, 10),
                       limits = c(-90, 0)) +
    labs(title = "Freezer temperature", x = "Time", y = "ºC") +
    theme_bw() +
    theme(
      plot.title = element_text(size = 18, face = "bold", hjust = 0.5),
      panel.border = element_blank(),
      panel.grid = element_blank(),
      axis.line = element_line(size = 2, color = "black"),
      axis.ticks = element_line(size = 2),
      axis.text = element_text(size = 12, face = "bold", color = "black"),
      axis.title = element_text(size = 14, face = "bold")
    ), tooltip = c("text")) %>%
    config(displayModeBar = FALSE)
  
  return(output_plot)
}


ui <- fluidPage(
  plotlyOutput("freezer_plot")
)

server <- function(input, output, session) {
  # Importing the data
  freezer_data <- import_dataset("1KpIEUuMpRD8q3DDNNUeJ1BqSztl_nAzA8DWtdTHFnVY")
  
  # Making the plot
 output$freezer_plot <- renderPlotly({
    make_temp_plot(freezer_data)
  })
}

shinyApp(ui, server)