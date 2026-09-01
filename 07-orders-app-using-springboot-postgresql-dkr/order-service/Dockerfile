FROM eclipse-temurin:17-jdk-jammy AS builder

WORKDIR /app

COPY order-service/src ./src
COPY order-service/pom.xml ./pom.xml
RUN apt-get update && apt-get install -y maven
RUN mvn clean package -DskipTests

FROM eclipse-temurin:17-jre-alpine

RUN addgroup -S spring && adduser -S spring -G spring

WORKDIR /app

COPY --from=builder /app/target/*.jar app.jar

USER spring

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]