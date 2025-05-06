docker build -t ecommerce-pesca:latest .
docker run -d -p 8080:80 ecommerce-pesca:latest
# teste no navegador http://localhost:8080
az login 
az group create --name dio-container-app --location eastus
az acr create --resource-group dio-container-app --name diocontainerdioacr --sku Basic
az acr login --name diocontainerdioacr

docker tag ecommerce-pesca:latest diocontainerdioacr.azurecr.io/ecommerce-pesca:latest
docker push diocontainerdioacr.azurecr.io/ecommerce-pesca:latest
az containerapp env create --name dio-container-app-env --resource-group dio-container-app --location eastus 
az containerapp create --name ecommerce-pesca --resource-group dio-container-app --environment dio-container-app-env --image diocontainerdioacr.azurecr.io/ecommerce-pesca:latest --target-port 80 --ingress external --registry-server diocontainerdioacr.azurecr.io --registry-username diocontainerdioacr --registry-password 'minha senha'
#nome da imagem e do container
# no dio-container-app abrir a pagina diocontairnecr e em repositories 
#clicar na imagem dio-container-app e depois em tags para ver as tags da imagem latest
# copiar container id (Referência de artefato): diocontainerdioacr.azurecr.io/ecommerce-pesca:latest
# diocontainerdioacr | Chaves de acesso | marcar ususário administador e copiar o nome de usuário e a senha
# usuário: diocontainerdioacr 
#senha: minha senha
#senha2: minha senha
# create environment variables containerapp
#az containerapp env create --name dio-container-app-env --resource-group dio-container-app --location eastus 
#az containerapp create --name dio-container-app --resource-group dio-container-app --environment dio-container-app-env --image diocontainerdioacr.azurecr.io/dio-container-app:latest --target-port 8080 --ingress external --registry-server diocontainerdioacr.azurecr.io --registry-username diocontainerdioacr --registry-password 'minha senha'
#--logs-instrumentation-key <instrumentation-key> --logs-workspace-id <workspace-id>
az acr repository list --name diocontainerdioacr --output table
az acr repository show-tags --name diocontainerdioacr --repository dio-container-app --output table
az acr repository show-manifests --name diocontainerdioacr --repository dio-container-app --output table