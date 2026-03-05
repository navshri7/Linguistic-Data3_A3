library(ggplot2)
library(dplyr)

data <- read.csv("dataset-t2.csv")

# question 1
ggplot(data, aes(x = RTlexdec)) + 
  geom_histogram(bins = 50, fill = "skyblue", color = "black") +
  theme_minimal() +
  labs(title = "Distribution of Reaction Times (RTlexdec)", x = "RT (ms)", y = "Frequency")

# question 2
ggplot(data, aes(x = RTlexdec)) + 
  geom_histogram(bins = 30, fill = "orange", color = "black") +
  facet_wrap(~AgeSubject) +
  theme_minimal() +
  labs(title = "RT Distribution by Age Group")

young_data <- subset(data, AgeSubject == "young")

# question 3
# (a) 
young_data$z_rt <- (young_data$RTlexdec - mean(young_data$RTlexdec)) / sd(young_data$RTlexdec)
# (b)
high_z <- mean(young_data$z_rt > 1.96) * 100
low_z <- mean(young_data$z_rt < -1.96) * 100
cat("Percentage of Z-scores > 1.96:", high_z, "%\n")
cat("Percentage of Z-scores < -1.96:", low_z, "%\n")
# (c) 
extreme_outliers <- subset(young_data, z_rt > 3)
print(extreme_outliers$Word)

# question 4
stats_compare <- data.frame(
  Metric = c("Mean", "Median"),
  RT = c(mean(young_data$RTlexdec), median(young_data$RTlexdec)),
  NounFreq = c(mean(young_data$NounFrequency, na.rm=T), median(young_data$NounFrequency, na.rm=T))
)
print(stats_compare)

# question 5
young_data$starts_with_p <- grepl("^p", young_data$Word, ignore.case = TRUE)
t_test_p <- t.test(RTlexdec ~ starts_with_p, data = young_data)
print(t_test_p)

# question 6
ggplot(young_data, aes(x = WordCategory, y = RTlexdec, fill = WordCategory)) + 
  geom_boxplot() +
  theme_minimal() +
  labs(title = "RT Comparison: Nouns vs Verbs")

cat("\nFive-number summary for Nouns:\n")
print(fivenum(young_data$RTlexdec[young_data$WordCategory == "N"]))

# question 7
ggplot(young_data, aes(x = WordCategory, y = RTlexdec)) +
  stat_summary(fun = mean, geom = "bar", fill = "lightgrey", color = "black") +
  stat_summary(fun.data = mean_cl_normal, geom = "errorbar", width = 0.2) +
  theme_minimal() +
  labs(title = "Mean RT with 95% CI")

# question 8
young_data$initial_letter <- substr(tolower(young_data$Word), 1, 1)
ggplot(young_data, aes(x = initial_letter, y = RTlexdec)) +
  geom_boxplot(fill = "lightblue") +
  theme_minimal() +
  labs(title = "RT by Initial Letter")

# question 9
young_data$two_consonants <- grepl("^[^aeiou]{2}", young_data$Word, ignore.case = TRUE)
t_test_cluster <- t.test(RTlexdec ~ two_consonants, data = young_data)
print(t_test_cluster)