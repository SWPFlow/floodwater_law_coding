
# Define everything in the global scope (meaning it is only executed once) here
# for less clutter, this is done in a separate script

source("global.R", encoding = "UTF-8")

# Define UI for app ----
ui <- fluidPage(
  
  # App title ----
  titlePanel("The network of Swiss floodwater regulation across laws"),
  hr(),
  # Sidebar layout with input and output definitions ----
  fluidRow(
    
    # Sidebar panel for inputs ----
    column(2,
      checkboxGroupInput(inputId = "issue_choice",
                  label = "Which floodwater issues should be displayed?",
                  choices = unique(el$issue),
                  selected = c("Auenschutz","Raumplanungsinstrumente","Naturgefahren"))),
    column(2, style = "background-color:#FDFBFA;",
      checkboxGroupInput(inputId = "law_choice",
                         label = "Which laws should be included?",
                         choices = lawname_list,
                         selected = lawname_list),
      checkboxInput(inputId = "label_articles","Should articles be labeled?", TRUE)
    ),
    # Main panel for displaying outputs ----
    column(8,
      plotOutput(outputId = "netplot")
      
    )
  )
)

# Define server logic ----

server <- function(input, output) {

# This reactive function subsets the edgelist every time the choice of issues is altered
    
  el_subset <- reactive({
    subset_el <- el[el$issue %in% input$issue_choice & 
                      grepl(pattern = paste(input$law_choice, collapse = "|"),
                            el$article),]
    subset_el
  })
  
  make_network <- reactive({
    plot_el <- el_subset()
    net <- network(plot_el)
    
    vertexnames <- get.vertex.attribute(net, "vertex.names")
    
    if (input$label_articles == FALSE){
      namevec <- ifelse(vertexnames %in% plot_el$issue, vertexnames, "")      
    }
    if (input$label_articles == TRUE){
      namevec <- vertexnames
    }
    colorvec <- ifelse(vertexnames %in% plot_el$issue, "#a53634","#002903")
    return(list(net = net, colorvec = colorvec, namevec = namevec))
  })
  
  output$netplot <- renderPlot({
    
    plotting_list <- make_network()
     
    ggnet2(plotting_list$net,
           node.color = plotting_list$colorvec, 
           node.label = plotting_list$namevec, 
           node.alpha = 0.5)
  })
  
}

shinyApp(ui = ui, server = server)
