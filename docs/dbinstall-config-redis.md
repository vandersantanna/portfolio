# 🔴 Redis - Guia Completo de Instalação e Configuração
## Cache em Memória de Alto Performance para Aplicações Modernas

---

## 🏆 Badges Profissionais

[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Redis Stack](https://img.shields.io/badge/Redis_Stack-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/docs/stack/)
[![Redis Cluster](https://img.shields.io/badge/Redis_Cluster-FF6600?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/topics/cluster-tutorial)
[![Redis Sentinel](https://img.shields.io/badge/Redis_Sentinel-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/topics/sentinel)
[![Redis Modules](https://img.shields.io/badge/Redis_Modules-FF6600?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/modules)

[![Documentation](https://img.shields.io/badge/Docs-Redis.io-blue?style=for-the-badge)](https://redis.io/documentation)
[![Commands](https://img.shields.io/badge/Commands-Reference-green?style=for-the-badge)](https://redis.io/commands)
[![Download](https://img.shields.io/badge/Download-Latest-red?style=for-the-badge)](https://redis.io/download)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/redis/redis)

---

## 📋 Table of Contents

1. [🎯 Overview](#-overview)
2. [✅ Prerequisites](#-prerequisites)
3. [🐧 Instalação no Linux](#-instalação-no-linux)
4. [🍎 Instalação no macOS](#-instalação-no-macos)
5. [🪟 Instalação no Windows](#-instalação-no-windows)
6. [⚙️ Configuração Básica](#️-configuração-básica)
7. [🔧 Configuração Avançada](#-configuração-avançada)
8. [🔒 Segurança](#-segurança)
9. [📊 Monitoramento](#-monitoramento)
10. [🚀 Performance](#-performance)
11. [🔄 Backup e Recovery](#-backup-e-recovery)
12. [🌐 Redis Cluster](#-redis-cluster)
13. [🛡️ Redis Sentinel](#️-redis-sentinel)
14. [🐳 Docker](#-docker)
15. [☁️ Cloud](#️-cloud)
16. [🧪 Testes](#-testes)
17. [❗ Troubleshooting](#-troubleshooting)
18. [📚 Recursos Adicionais](#-recursos-adicionais)

---

## 🎯 Overview

O **Redis** (Remote Dictionary Server) é um banco de dados em memória de código aberto usado como cache, broker de mensagens e base de dados. É conhecido por sua velocidade excepcional e versatilidade.

### 🌟 Features Principais

- **⚡ Performance Ultra-Rápida**: Operações em microssegundos
- **🗂️ Estruturas de Dados Avançadas**: Strings, Lists, Sets, Hashes, Sorted Sets
- **🔄 Persistência Configurável**: RDB snapshots e AOF logs
- **🌐 Clustering**: Distribuição automática de dados
- **🛡️ Alta Disponibilidade**: Redis Sentinel para failover
- **📡 Pub/Sub**: Sistema de mensageria em tempo real
- **🔍 Módulos**: Extensibilidade com RedisJSON, RedisSearch, etc.
- **🐳 Container Ready**: Suporte completo ao Docker
- **☁️ Cloud Native**: Integração com AWS, Azure, GCP

### 📈 Casos de Uso

- **Cache de Aplicação**: Redução de latência
- **Session Store**: Gerenciamento de sessões
- **Message Broker**: Filas e pub/sub
- **Real-time Analytics**: Contadores e métricas
- **Leaderboards**: Rankings em tempo real
- **Rate Limiting**: Controle de taxa de requisições

---

## ✅ Prerequisites

### 🖥️ Sistemas Operacionais Suportados

| Sistema | Versões | Status | Notas |
|---------|---------|--------|-------|
| **Ubuntu** | 18.04+ | ✅ Oficial | Recomendado para produção |
| **CentOS/RHEL** | 7+ | ✅ Oficial | Suporte empresarial |
| **Debian** | 9+ | ✅ Oficial | Estável e confiável |
| **Amazon Linux** | 2 | ✅ Oficial | Otimizado para AWS |
| **macOS** | 10.14+ | ✅ Oficial | Via Homebrew |
| **Windows** | 10/11 | ⚠️ Via WSL | Recomendado WSL2 |
| **Docker** | Qualquer | ✅ Oficial | Multiplataforma |

### 🔧 Requisitos de Hardware

#### **Mínimo (Desenvolvimento)**
- **RAM**: 1GB
- **CPU**: 1 core
- **Storage**: 5GB
- **Network**: 100Mbps

#### **Recomendado (Produção)**
- **RAM**: 8GB+ (preferível SSD como swap)
- **CPU**: 4+ cores
- **Storage**: SSD NVMe
- **Network**: 1Gbps+

### 📦 Dependências de Sistema

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y build-essential tcl wget curl

# CentOS/RHEL
sudo yum groupinstall -y "Development Tools"
sudo yum install -y tcl wget curl

# macOS
xcode-select --install
```
## 🐧 Instalação no Linux

### 📦 Método 1: Package Manager (Recomendado)

#### Ubuntu/Debian
```bash
# Atualizar repositórios
sudo apt update

# Instalar Redis
sudo apt install -y redis-server redis-tools

# Verificar instalação
redis-cli --version
sudo systemctl status redis-server
```

#### CentOS/RHEL 8+
```bash
# Habilitar EPEL
sudo dnf install -y epel-release

# Instalar Redis
sudo dnf install -y redis redis-tools

# Iniciar e habilitar
sudo systemctl start redis
sudo systemctl enable redis
```

#### CentOS/RHEL 7
```bash
# Habilitar EPEL
sudo yum install -y epel-release

# Instalar Redis
sudo yum install -y redis redis-tools

# Iniciar e habilitar
sudo systemctl start redis
sudo systemctl enable redis
```

### 🔧 Método 2: Compilação from Source

#### Download e Compilação
```bash
# Criar diretório de trabalho
mkdir ~/redis-build && cd ~/redis-build

# Download da versão estável
wget http://download.redis.io/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable

# Compilar
make

# Executar testes (opcional mas recomendado)
make test

# Instalar
sudo make install

# Criar diretórios
sudo mkdir -p /etc/redis
sudo mkdir -p /var/lib/redis
sudo mkdir -p /var/log/redis
```

#### Configurar Usuário Redis
```bash
# Criar usuário redis
sudo useradd --system --home /var/lib/redis --shell /bin/false redis

# Definir permissões
sudo chown redis:redis /var/lib/redis
sudo chown redis:redis /var/log/redis
sudo chmod 750 /var/lib/redis
sudo chmod 755 /var/log/redis
```

### ⚙️ Configuração Inicial

#### Arquivo de Configuração Principal
```bash
# Copiar configuração padrão
sudo cp redis.conf /etc/redis/redis.conf

# Backup da configuração original
sudo cp /etc/redis/redis.conf /etc/redis/redis.conf.backup
```

#### Configurações Essenciais
```bash
# Editar configuração
sudo nano /etc/redis/redis.conf

# Principais alterações:
```

```conf
# /etc/redis/redis.conf

# Bind para interface específica (segurança)
bind 127.0.0.1 ::1

# Porta padrão
port 6379

# Executar como daemon
daemonize yes

# Arquivo PID
pidfile /var/run/redis/redis-server.pid

# Log level
loglevel notice

# Arquivo de log
logfile /var/log/redis/redis-server.log

# Diretório de trabalho
dir /var/lib/redis

# Arquivo de dump RDB
dbfilename dump.rdb

# Configuração de memória
maxmemory 2gb
maxmemory-policy allkeys-lru

# Configurações de rede
timeout 0
tcp-keepalive 300

# Configurações de persistência RDB
save 900 1
save 300 10
save 60 10000

# Configuração AOF
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
```

### 🔄 Systemd Service

#### Criar arquivo de serviço
```bash
sudo nano /etc/systemd/system/redis.service
```

```ini
[Unit]
Description=Redis In-Memory Data Store
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
ExecStop=/usr/local/bin/redis-cli shutdown
Restart=always
RestartSec=3
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

#### Habilitar e iniciar serviço
```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar inicialização automática
sudo systemctl enable redis

# Iniciar Redis
sudo systemctl start redis

# Verificar status
sudo systemctl status redis

# Ver logs
sudo journalctl -u redis -f
```

### 🧪 Verificação da Instalação

#### Testes Básicos
```bash
# Conectar ao Redis
redis-cli

# Dentro do redis-cli:
127.0.0.1:6379> ping
# Resposta: PONG

127.0.0.1:6379> set test "Hello Redis"
# Resposta: OK

127.0.0.1:6379> get test
# Resposta: "Hello Redis"

127.0.0.1:6379> info server
# Mostra informações do servidor

127.0.0.1:6379> exit
```

#### Verificar Performance
```bash
# Benchmark básico
redis-benchmark -q -n 100000

# Benchmark específico
redis-benchmark -t set,get -n 100000 -q

# Teste de latência
redis-cli --latency-history -h 127.0.0.1 -p 6379
```

## 🍎 Instalação no macOS

### 🍺 Método 1: Homebrew (Recomendado)

```bash
# Instalar Homebrew (se necessário)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Atualizar Homebrew
brew update

# Instalar Redis
brew install redis

# Verificar instalação
redis-server --version
redis-cli --version
```

### 🚀 Inicialização e Controle

```bash
# Iniciar Redis manualmente
redis-server

# Iniciar como serviço (background)
brew services start redis

# Parar serviço
brew services stop redis

# Reiniciar serviço
brew services restart redis

# Status do serviço
brew services list | grep redis
```

### ⚙️ Configuração macOS

```bash
# Localizar arquivo de configuração
find /usr/local -name "redis.conf" 2>/dev/null
# ou
find /opt/homebrew -name "redis.conf" 2>/dev/null

# Editar configuração
nano /usr/local/etc/redis.conf
# ou para Apple Silicon:
nano /opt/homebrew/etc/redis.conf
```

### 🔧 Método 2: Compilação Manual

```bash
# Instalar dependências
xcode-select --install

# Download e compilação
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable
make

# Instalar
sudo make install

# Criar diretórios
sudo mkdir -p /usr/local/etc/redis
sudo mkdir -p /usr/local/var/db/redis
sudo mkdir -p /usr/local/var/log
```
## 🪟 Instalação no Windows

### 🐧 Método 1: WSL2 (Recomendado)

```powershell
# Instalar WSL2
wsl --install

# Reiniciar e configurar Ubuntu
wsl --set-default-version 2
wsl --install -d Ubuntu-22.04

# Entrar no WSL
wsl
```

```bash
# Dentro do WSL - seguir instalação Linux
sudo apt update
sudo apt install -y redis-server redis-tools

# Iniciar Redis
sudo service redis-server start

# Verificar
redis-cli ping
```

### 🐳 Método 2: Docker Desktop

```powershell
# Instalar Docker Desktop
# Download: https://www.docker.com/products/docker-desktop

# Executar Redis
docker run --name redis-server -p 6379:6379 -d redis:latest

# Conectar
docker exec -it redis-server redis-cli
```

### 📦 Método 3: Binários Nativos (Desenvolvimento)

```powershell
# Download dos binários Windows
# https://github.com/microsoftarchive/redis/releases

# Extrair para C:\Redis
# Adicionar ao PATH do sistema

# Executar
redis-server.exe

# Em outro terminal
redis-cli.exe
```

---

## 🐳 Docker

### 🚀 Configuração Básica

#### Docker Compose Simples
```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    container_name: redis-server
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  redis_data:
```

#### Executar
```bash
# Iniciar
docker-compose up -d

# Verificar logs
docker-compose logs -f redis

# Conectar
docker-compose exec redis redis-cli

# Parar
docker-compose down
```

### 🔧 Configuração Avançada com Docker

#### Docker Compose Completo
```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    container_name: redis-server
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - ./redis.conf:/etc/redis/redis.conf:ro
      - redis_data:/data
      - redis_logs:/var/log/redis
    command: redis-server /etc/redis/redis.conf
    sysctls:
      - net.core.somaxconn=65535
    ulimits:
      memlock: -1
      nofile:
        soft: 65535
        hard: 65535
    environment:
      - REDIS_REPLICATION_MODE=master
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: redis-commander
    restart: unless-stopped
    environment:
      - REDIS_HOSTS=local:redis:6379
    ports:
      - "8081:8081"
    depends_on:
      - redis

volumes:
  redis_data:
  redis_logs:

networks:
  default:
    name: redis-network
```

#### Configuração Redis para Docker
```conf
# redis.conf
bind 0.0.0.0
port 6379
daemonize no
pidfile /var/run/redis/redis-server.pid
loglevel notice
logfile /var/log/redis/redis-server.log
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data
maxmemory 1gb
maxmemory-policy allkeys-lru
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 100
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
```

---

## ⚙️ Configuração Básica

### 📝 Estrutura de Configuração

```conf
# /etc/redis/redis.conf

################################## NETWORK #####################################
# Interface de rede
bind 127.0.0.1 ::1

# Porta
port 6379

# Timeout de conexão inativa (0 = desabilitado)
timeout 0

# TCP keepalive
tcp-keepalive 300

################################# GENERAL #####################################
# Executar como daemon
daemonize yes

# Arquivo PID
pidfile /var/run/redis/redis-server.pid

# Log level: debug, verbose, notice, warning
loglevel notice

# Arquivo de log
logfile /var/log/redis/redis-server.log

# Número de databases
databases 16

################################ SNAPSHOTTING  ################################
# Salvar snapshot se:
# - Pelo menos 1 key mudou em 900 segundos (15 min)
# - Pelo menos 10 keys mudaram em 300 segundos (5 min)  
# - Pelo menos 10000 keys mudaram em 60 segundos
save 900 1
save 300 10
save 60 10000

# Parar escritas se snapshot falhar
stop-writes-on-bgsave-error yes

# Comprimir snapshots RDB
rdbcompression yes

# Checksum do RDB
rdbchecksum yes

# Nome do arquivo RDB
dbfilename dump.rdb

# Diretório de trabalho
dir /var/lib/redis

################################# REPLICATION #################################
# Configuração de replica (se aplicável)
# replicaof <masterip> <masterport>

# Senha do master (se aplicável)
# masterauth <master-password>

################################## SECURITY ###################################
# Require password
# requirepass yourpassword

# Comandos perigosos
# rename-command FLUSHDB ""
# rename-command FLUSHALL ""
# rename-command DEBUG ""

################################### CLIENTS ####################################
# Máximo de clientes conectados
# maxclients 10000

############################## MEMORY MANAGEMENT #############################
# Limite de memória
maxmemory 2gb

# Política quando limite é atingido
maxmemory-policy allkeys-lru

############################# LAZY FREEING ####################################
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no

############################ KERNEL OOM CONTROL ##############################
oom-score-adj no

############################## APPEND ONLY MODE ###############################
# Habilitar AOF
appendonly yes

# Nome do arquivo AOF
appendfilename "appendonly.aof"

# Frequência de fsync
appendfsync everysec

# Não fazer fsync durante rewrite
no-appendfsync-on-rewrite no

# Auto rewrite do AOF
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Carregar AOF truncado
aof-load-truncated yes

# Usar RDB+AOF para persistence
aof-use-rdb-preamble yes

################################ LUA SCRIPTING  ###############################
# Timeout para scripts Lua
lua-time-limit 5000

################################## SLOW LOG ###################################
# Log de comandos lentos (microssegundos)
slowlog-log-slower-than 10000

# Tamanho máximo do slow log
slowlog-max-len 128

################################ LATENCY MONITOR ##############################
# Monitor de latência (microssegundos)
latency-monitor-threshold 100
```

### 🔒 Configurações de Segurança Básica

```conf
# Senha forte
requirepass "Sup3rS3cur3P@ssw0rd!"

# Bind apenas interfaces necessárias
bind 127.0.0.1 10.0.0.100

# Desabilitar comandos perigosos
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command DEBUG ""
rename-command CONFIG "CONFIG_09f911029d74e35bd84156c5635688c0"

# Modo protegido
protected-mode yes

# Timeout de cliente
timeout 300
```

### 📊 Configurações de Performance

```conf
# Otimizações de memória
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64

# Buffer de saída para clientes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60

# Frequency de operações de background
hz 10

# Rehashing ativo
activerehashing yes

# AOF incremental fsync
aof-rewrite-incremental-fsync yes
```
## 🔧 Configuração Avançada

### 🏗️ Redis Sentinel (Alta Disponibilidade)

#### Configuração Master
```conf
# /etc/redis/redis-master.conf
port 6379
bind 0.0.0.0
requirepass "master-password"
masterauth "master-password"
```

#### Configuração Replica
```conf
# /etc/redis/redis-replica.conf
port 6380
bind 0.0.0.0
replicaof 192.168.1.100 6379
requirepass "replica-password"
masterauth "master-password"
```

#### Configuração Sentinel
```conf
# /etc/redis/sentinel.conf
port 26379
bind 0.0.0.0
sentinel monitor mymaster 192.168.1.100 6379 2
sentinel auth-pass mymaster master-password
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 10000
sentinel deny-scripts-reconfig yes
```

#### Iniciar Sentinel
```bash
redis-sentinel /etc/redis/sentinel.conf
```

---

## 🌐 Redis Cluster

### 🔧 Configuração de Cluster (6 Nós)

#### Configuração Base para Cluster
```conf
# /etc/redis/redis-cluster-700X.conf (para cada nó)
port 7001  # 7001, 7002, 7003, 7004, 7005, 7006
bind 0.0.0.0
cluster-enabled yes
cluster-config-file nodes-7001.conf  # unique para cada nó
cluster-node-timeout 15000
appendonly yes
```

#### Script de Inicialização do Cluster
```bash
#!/bin/bash
# cluster-setup.sh

# Criar diretórios
for port in {7001..7006}; do
    mkdir -p /etc/redis/cluster/$port
    mkdir -p /var/lib/redis/cluster/$port
    mkdir -p /var/log/redis/cluster
done

# Copiar configurações
for port in {7001..7006}; do
    sed "s/7001/$port/g" /etc/redis/redis-cluster-template.conf > /etc/redis/cluster/$port/redis.conf
done

# Iniciar nós
for port in {7001..7006}; do
    redis-server /etc/redis/cluster/$port/redis.conf
done

# Criar cluster
redis-cli --cluster create \
    127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 \
    127.0.0.1:7004 127.0.0.1:7005 127.0.0.1:7006 \
    --cluster-replicas 1
```

#### Gerenciamento do Cluster
```bash
# Verificar status
redis-cli --cluster check 127.0.0.1:7001

# Informações do cluster
redis-cli -c -p 7001
127.0.0.1:7001> CLUSTER NODES
127.0.0.1:7001> CLUSTER INFO

# Adicionar nó
redis-cli --cluster add-node 127.0.0.1:7007 127.0.0.1:7001

# Remover nó
redis-cli --cluster del-node 127.0.0.1:7001 <node-id>

# Rebalancear
redis-cli --cluster rebalance 127.0.0.1:7001
```

---

## 🔒 Segurança

### 🛡️ Configuração Avançada de Segurança

```conf
# /etc/redis/redis-secure.conf

# Autenticação
requirepass "Sup3rS3cur3P@ssw0rd!2024"
masterauth "Sup3rS3cur3P@ssw0rd!2024"

# Network Security
bind 127.0.0.1 10.0.0.100
protected-mode yes
port 0  # Desabilitar porta padrão
tls-port 6380  # Usar TLS

# TLS Configuration
tls-cert-file /etc/redis/tls/redis.crt
tls-key-file /etc/redis/tls/redis.key
tls-ca-cert-file /etc/redis/tls/ca.crt
tls-protocols "TLSv1.2 TLSv1.3"

# Command Security
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command DEBUG ""
rename-command EVAL ""
rename-command CONFIG "CONFIG_$(openssl rand -hex 16)"
rename-command SHUTDOWN "SHUTDOWN_$(openssl rand -hex 16)"

# Access Control Lists (Redis 6+)
user default off
user admin on >admin-password ~* &* +@all
user readonly on >readonly-password ~* &* +@read
user app on >app-password ~app:* &* +@read +@write -@dangerous
```

### 🔐 Configurar TLS/SSL

```bash
# Gerar certificados
mkdir -p /etc/redis/tls
cd /etc/redis/tls

# CA privada
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt

# Certificado do servidor
openssl genrsa -out redis.key 4096
openssl req -new -key redis.key -out redis.csr
openssl x509 -req -in redis.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out redis.crt -days 365 -sha256

# Definir permissões
chown redis:redis /etc/redis/tls/*
chmod 600 /etc/redis/tls/*.key
chmod 644 /etc/redis/tls/*.crt
```

---

## 📊 Monitoramento

### 📈 Ferramentas de Monitoramento

#### Redis INFO
```bash
# Informações gerais
redis-cli info

# Seções específicas
redis-cli info memory
redis-cli info stats
redis-cli info replication
redis-cli info persistence
redis-cli info clients
redis-cli info server
```

#### Comandos de Monitoramento
```bash
# Monitor em tempo real
redis-cli monitor

# Estatísticas de comandos
redis-cli --stat

# Latência
redis-cli --latency
redis-cli --latency-history

# Big keys
redis-cli --bigkeys

# Memória por chave
redis-cli --memkeys

# Scan de padrões
redis-cli --scan --pattern "user:*"
```

### 📊 Scripts de Monitoramento

#### Script de Métricas
```bash
#!/bin/bash
# redis-metrics.sh

REDIS_CLI="redis-cli"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== Redis Metrics - $DATE ==="

# Informações básicas
echo "--- Server Info ---"
$REDIS_CLI info server | grep -E "(redis_version|uptime_in_days|process_id)"

# Memória
echo -e "\n--- Memory Usage ---"
$REDIS_CLI info memory | grep -E "(used_memory_human|used_memory_peak_human|mem_fragmentation_ratio)"

# Estatísticas
echo -e "\n--- Stats ---"
$REDIS_CLI info stats | grep -E "(total_connections_received|total_commands_processed|instantaneous_ops_per_sec)"

# Clientes
echo -e "\n--- Clients ---"
$REDIS_CLI info clients | grep -E "(connected_clients|blocked_clients)"

# Persistência
echo -e "\n--- Persistence ---"
$REDIS_CLI info persistence | grep -E "(rdb_last_save_time|aof_enabled)"

# Keyspace
echo -e "\n--- Keyspace ---"
$REDIS_CLI info keyspace
```

#### Alertas Básicos
```bash
#!/bin/bash
# redis-alerts.sh

REDIS_CLI="redis-cli"
MEMORY_THRESHOLD=80
CLIENT_THRESHOLD=1000

# Verificar uso de memória
MEMORY_USAGE=$($REDIS_CLI info memory | grep used_memory_rss | cut -d: -f2 | tr -d '\r')
MAX_MEMORY=$($REDIS_CLI config get maxmemory | tail -1)

if [ "$MAX_MEMORY" != "0" ]; then
    MEMORY_PERCENT=$((MEMORY_USAGE * 100 / MAX_MEMORY))
    if [ $MEMORY_PERCENT -gt $MEMORY_THRESHOLD ]; then
        echo "ALERT: Redis memory usage is ${MEMORY_PERCENT}% (threshold: ${MEMORY_THRESHOLD}%)"
    fi
fi

# Verificar número de clientes
CLIENTS=$($REDIS_CLI info clients | grep connected_clients | cut -d: -f2 | tr -d '\r')
if [ $CLIENTS -gt $CLIENT_THRESHOLD ]; then
    echo "ALERT: Too many clients connected: $CLIENTS (threshold: $CLIENT_THRESHOLD)"
fi
```

---

## 🔄 Backup e Recovery

### 💾 Backup RDB

#### Backup Manual
```bash
#!/bin/bash
# redis-backup.sh

BACKUP_DIR="/backup/redis"
DATE=$(date +%Y%m%d_%H%M%S)
REDIS_CLI="redis-cli"

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Forçar snapshot
$REDIS_CLI BGSAVE

# Aguardar conclusão
while [ $($REDIS_CLI LASTSAVE) -eq $($REDIS_CLI LASTSAVE) ]; do
    sleep 1
done

# Copiar dump
cp /var/lib/redis/dump.rdb $BACKUP_DIR/dump_$DATE.rdb

# Comprimir
gzip $BACKUP_DIR/dump_$DATE.rdb

# Limpar backups antigos (manter 7 dias)
find $BACKUP_DIR -name "dump_*.rdb.gz" -mtime +7 -delete

echo "Backup completed: dump_$DATE.rdb.gz"
```

#### Backup Automático com Cron
```bash
# Adicionar ao crontab
crontab -e

# Backup diário às 2:00
0 2 * * * /scripts/redis-backup.sh

# Backup de hora em hora durante horário comercial
0 9-18 * * 1-5 /scripts/redis-backup.sh
```

### 📁 Backup AOF

#### Script de Backup AOF
```bash
#!/bin/bash
# redis-aof-backup.sh

BACKUP_DIR="/backup/redis/aof"
DATE=$(date +%Y%m%d_%H%M%S)
REDIS_CLI="redis-cli"

mkdir -p $BACKUP_DIR

# Rewrite AOF
$REDIS_CLI BGREWRITEAOF

# Aguardar conclusão
while [ $($REDIS_CLI info persistence | grep aof_rewrite_in_progress | cut -d: -f2 | tr -d '\r') -eq 1 ]; do
    sleep 1
done

# Copiar AOF
cp /var/lib/redis/appendonly.aof $BACKUP_DIR/appendonly_$DATE.aof
gzip $BACKUP_DIR/appendonly_$DATE.aof

echo "AOF backup completed: appendonly_$DATE.aof.gz"
```

### 🔄 Recovery

#### Recovery de RDB
```bash
#!/bin/bash
# redis-restore-rdb.sh

BACKUP_FILE="$1"
REDIS_DATA_DIR="/var/lib/redis"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.rdb.gz>"
    exit 1
fi

# Parar Redis
sudo systemctl stop redis

# Backup atual
mv $REDIS_DATA_DIR/dump.rdb $REDIS_DATA_DIR/dump.rdb.backup.$(date +%s)

# Restaurar backup
gunzip -c $BACKUP_FILE > $REDIS_DATA_DIR/dump.rdb
chown redis:redis $REDIS_DATA_DIR/dump.rdb

# Iniciar Redis
sudo systemctl start redis

echo "Recovery completed from $BACKUP_FILE"
```

#### Recovery de AOF
```bash
#!/bin/bash
# redis-restore-aof.sh

BACKUP_FILE="$1"
REDIS_DATA_DIR="/var/lib/redis"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.aof.gz>"
    exit 1
fi

# Parar Redis
sudo systemctl stop redis

# Backup atual
mv $REDIS_DATA_DIR/appendonly.aof $REDIS_DATA_DIR/appendonly.aof.backup.$(date +%s)

# Restaurar backup
gunzip -c $BACKUP_FILE > $REDIS_DATA_DIR/appendonly.aof
chown redis:redis $REDIS_DATA_DIR/appendonly.aof

# Verificar integridade
redis-check-aof --fix $REDIS_DATA_DIR/appendonly.aof

# Iniciar Redis
sudo systemctl start redis

echo "AOF recovery completed from $BACKUP_FILE"
```

## 🚀 Performance

### ⚡ Otimização de Sistema Operacional

#### Configurações de Kernel
```bash
# /etc/sysctl.conf
# Otimizações para Redis

# Memory overcommit
vm.overcommit_memory = 1

# Transparent Huge Pages (desabilitar)
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

# Network optimizations
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535

# File descriptors
fs.file-max = 65535
```

#### Configurações Permanentes
```bash
# /etc/security/limits.conf
redis soft nofile 65535
redis hard nofile 65535
redis soft nproc 65535
redis hard nproc 65535

# Aplicar configurações
sudo sysctl -p
sudo systemctl restart redis
```

### 🔧 Tuning de Performance

#### Configurações Redis para Performance
```conf
# /etc/redis/redis-performance.conf

# TCP settings
tcp-backlog 65535
tcp-keepalive 60

# Client settings
timeout 300
maxclients 50000

# Memory settings
maxmemory 8gb
maxmemory-policy allkeys-lru
maxmemory-samples 5

# Persistence tuning
save 900 1
save 300 10
save 60 10000
rdbcompression yes
rdbchecksum no  # Desabilitar para performance

# AOF tuning
appendonly yes
appendfsync everysec
no-appendfsync-on-rewrite yes
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Background operations
hz 10
activerehashing yes

# Data structure optimizations
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64

# Lazy freeing
lazyfree-lazy-eviction yes
lazyfree-lazy-expire yes
lazyfree-lazy-server-del yes
replica-lazy-flush yes

# Client buffer limits
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
```

### 📊 Benchmarking

#### Scripts de Benchmark
```bash
#!/bin/bash
# redis-benchmark-suite.sh

echo "=== Redis Performance Benchmark ==="
date

# Benchmark básico
echo -e "\n--- Basic Operations ---"
redis-benchmark -q -n 100000 -c 50 -t set,get,incr,lpush,rpush,lpop,rpop,sadd,hset,spop,zadd,zpopmin,lrange

# Benchmark de pipeline
echo -e "\n--- Pipeline Performance ---"
redis-benchmark -q -n 100000 -c 50 -P 16 -t set,get

# Benchmark de diferentes tamanhos de dados
echo -e "\n--- Data Size Performance ---"
for size in 10 100 1000 10000; do
    echo "Data size: $size bytes"
    redis-benchmark -q -n 10000 -d $size -t set,get
done

# Benchmark específico por operação
echo -e "\n--- Detailed Operation Benchmark ---"
redis-benchmark -n 100000 -t set
redis-benchmark -n 100000 -t get
redis-benchmark -n 100000 -t incr
redis-benchmark -n 100000 -t lpush
redis-benchmark -n 100000 -t rpush
redis-benchmark -n 100000 -t lpop
redis-benchmark -n 100000 -t rpop
redis-benchmark -n 100000 -t sadd
redis-benchmark -n 100000 -t hset
redis-benchmark -n 100000 -t spop
redis-benchmark -n 100000 -t zadd
redis-benchmark -n 100000 -t zpopmin
redis-benchmark -n 100000 -t lrange -r 100
```

---

## 🧪 Testes

### 🔍 Scripts de Teste

#### Teste de Funcionalidade
```bash
#!/bin/bash
# redis-functional-test.sh

REDIS_CLI="redis-cli"
TEST_KEY="test:$(date +%s)"

echo "=== Redis Functional Tests ==="

# Teste de conectividade
echo -n "Testing connectivity... "
if $REDIS_CLI ping | grep -q PONG; then
    echo "✅ PASSED"
else
    echo "❌ FAILED"
    exit 1
fi

# Teste de operações básicas
echo -n "Testing basic operations... "
$REDIS_CLI set $TEST_KEY "test_value" > /dev/null
if [ "$($REDIS_CLI get $TEST_KEY)" = "test_value" ]; then
    echo "✅ PASSED"
else
    echo "❌ FAILED"
fi

# Teste de expiração
echo -n "Testing expiration... "
$REDIS_CLI setex ${TEST_KEY}_exp 2 "expire_test" > /dev/null
sleep 3
if [ "$($REDIS_CLI get ${TEST_KEY}_exp)" = "" ]; then
    echo "✅ PASSED"
else
    echo "❌ FAILED"
fi

# Teste de estruturas de dados
echo -n "Testing data structures... "
$REDIS_CLI lpush ${TEST_KEY}_list "item1" "item2" > /dev/null
$REDIS_CLI sadd ${TEST_KEY}_set "member1" "member2" > /dev/null
$REDIS_CLI hset ${TEST_KEY}_hash "field1" "value1" > /dev/null

if [ "$($REDIS_CLI llen ${TEST_KEY}_list)" = "2" ] && \
   [ "$($REDIS_CLI scard ${TEST_KEY}_set)" = "2" ] && \
   [ "$($REDIS_CLI hlen ${TEST_KEY}_hash)" = "1" ]; then
    echo "✅ PASSED"
else
    echo "❌ FAILED"
fi

# Limpeza
$REDIS_CLI del $TEST_KEY ${TEST_KEY}_list ${TEST_KEY}_set ${TEST_KEY}_hash > /dev/null

echo "All tests completed!"
```

#### Teste de Carga
```bash
#!/bin/bash
# redis-load-test.sh

REDIS_CLI="redis-cli"
CONCURRENT_CLIENTS=50
OPERATIONS_PER_CLIENT=1000

echo "=== Redis Load Test ==="
echo "Clients: $CONCURRENT_CLIENTS"
echo "Operations per client: $OPERATIONS_PER_CLIENT"

# Função de teste por cliente
test_client() {
    local client_id=$1
    local prefix="load_test_${client_id}"
    
    for i in $(seq 1 $OPERATIONS_PER_CLIENT); do
        $REDIS_CLI set "${prefix}_${i}" "value_${i}" > /dev/null
        $REDIS_CLI get "${prefix}_${i}" > /dev/null
        $REDIS_CLI del "${prefix}_${i}" > /dev/null
    done
}

# Executar clientes em paralelo
echo "Starting load test..."
start_time=$(date +%s)

for client in $(seq 1 $CONCURRENT_CLIENTS); do
    test_client $client &
done

# Aguardar conclusão
wait

end_time=$(date +%s)
total_time=$((end_time - start_time))
total_ops=$((CONCURRENT_CLIENTS * OPERATIONS_PER_CLIENT * 3))  # 3 ops per iteration

echo "Load test completed!"
echo "Total time: ${total_time}s"
echo "Total operations: $total_ops"
echo "Operations per second: $((total_ops / total_time))"
```

---

## ☁️ Cloud

### ☁️ AWS ElastiCache

#### Configuração via AWS CLI
```bash
# Criar subnet group
aws elasticache create-cache-subnet-group \
    --cache-subnet-group-name my-redis-subnet-group \
    --cache-subnet-group-description "Redis subnet group" \
    --subnet-ids subnet-12345678 subnet-87654321

# Criar cluster Redis
aws elasticache create-cache-cluster \
    --cache-cluster-id my-redis-cluster \
    --engine redis \
    --engine-version 7.0 \
    --cache-node-type cache.t3.micro \
    --num-cache-nodes 1 \
    --cache-subnet-group-name my-redis-subnet-group \
    --security-group-ids sg-12345678

# Criar replication group
aws elasticache create-replication-group \
    --replication-group-id my-redis-rg \
    --replication-group-description "Redis replication group" \
    --primary-cluster-id my-redis-cluster \
    --num-cache-clusters 3 \
    --engine redis \
    --engine-version 7.0 \
    --cache-node-type cache.r6g.large \
    --automatic-failover-enabled \
    --multi-az-enabled
```

#### Terraform para ElastiCache
```hcl
# terraform/redis.tf
resource "aws_elasticache_subnet_group" "redis" {
  name       = "redis-subnet-group"
  subnet_ids = var.private_subnet_ids
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id         = "redis-cluster"
  description                  = "Redis cluster"
  
  node_type                    = "cache.r6g.large"
  port                         = 6379
  parameter_group_name         = "default.redis7"
  
  num_cache_clusters           = 2
  automatic_failover_enabled   = true
  multi_az_enabled            = true
  
  subnet_group_name           = aws_elasticache_subnet_group.redis.name
  security_group_ids          = [aws_security_group.redis.id]
  
  at_rest_encryption_enabled  = true
  transit_encryption_enabled  = true
  auth_token                  = var.redis_auth_token
  
  apply_immediately           = false
  
  log_delivery_configuration {
    destination      = aws_cloudwatch_log_group.redis.name
    destination_type = "cloudwatch-logs"
    log_format       = "text"
    log_type         = "slow-log"
  }
  
  tags = {
    Name        = "redis-cluster"
    Environment = var.environment
  }
}

resource "aws_security_group" "redis" {
  name_prefix = "redis-"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 🔷 Azure Cache for Redis

#### Azure CLI
```bash
# Criar resource group
az group create --name rg-redis --location eastus

# Criar Azure Cache for Redis
az redis create \
    --resource-group rg-redis \
    --name my-redis-cache \
    --location eastus \
    --sku Premium \
    --vm-size P1 \
    --enable-non-ssl-port \
    --redis-configuration maxmemory-policy=allkeys-lru
```

### 🌐 Google Cloud Memorystore

#### gcloud CLI
```bash
# Criar instância Redis
gcloud redis instances create my-redis-instance \
    --size=1 \
    --region=us-central1 \
    --redis-version=redis_6_x \
    --enable-auth
```

---

## ❗ Troubleshooting

### 🔍 Problemas Comuns

#### Performance Issues
```bash
# Verificar slow queries
redis-cli slowlog get 10

# Verificar memory usage
redis-cli info memory

# Verificar latência
redis-cli --latency

# Big keys que consomem memória
redis-cli --bigkeys

# Monitor em tempo real
redis-cli monitor
```

#### Connection Issues
```bash
# Verificar se Redis está rodando
systemctl status redis

# Verificar portas
netstat -tlnp | grep 6379

# Teste de conectividade
telnet localhost 6379

# Verificar logs
tail -f /var/log/redis/redis-server.log

# Verificar configuração
redis-cli config get "*"
```

#### Memory Issues
```bash
# Verificar uso de memória
redis-cli info memory | grep used_memory_human

# Verificar fragmentação
redis-cli info memory | grep mem_fragmentation_ratio

# Limpar memória expirada
redis-cli --eval "return redis.call('memory', 'purge')" 0
```

### 🛠️ Scripts de Diagnóstico

#### Diagnóstico Completo
```bash
#!/bin/bash
# redis-diagnostic.sh

echo "=== Redis Diagnostic Report ==="
date
echo

# Verificar processo
echo "--- Process Status ---"
if pgrep redis-server > /dev/null; then
    echo "✅ Redis process is running"
    ps aux | grep redis-server | grep -v grep
else
    echo "❌ Redis process is not running"
fi
echo

# Verificar conectividade
echo "--- Connectivity Test ---"
if redis-cli ping | grep -q PONG; then
    echo "✅ Redis is responding"
else
    echo "❌ Redis is not responding"
fi
echo

# Informações do servidor
echo "--- Server Information ---"
redis-cli info server | grep -E "(redis_version|uptime_in_days|os)"
echo

# Uso de memória
echo "--- Memory Usage ---"
redis-cli info memory | grep -E "(used_memory_human|used_memory_peak_human|mem_fragmentation_ratio)"
echo

# Estatísticas
echo "--- Performance Stats ---"
redis-cli info stats | grep -E "(total_commands_processed|instantaneous_ops_per_sec|keyspace_hits|keyspace_misses)"
echo

# Clientes conectados
echo "--- Client Information ---"
redis-cli info clients
echo

# Configuração crítica
echo "--- Critical Configuration ---"
redis-cli config get maxmemory
redis-cli config get maxmemory-policy
redis-cli config get save
echo

# Slow log
echo "--- Recent Slow Queries ---"
redis-cli slowlog get 5
echo

# Keyspace
echo "--- Keyspace Information ---"
redis-cli info keyspace
```

---

## 📚 Recursos Adicionais

### 🔗 Links Oficiais

- **[Redis.io](https://redis.io/)** - Site oficial
- **[Documentação](https://redis.io/documentation)** - Documentação completa
- **[Commands Reference](https://redis.io/commands)** - Referência de comandos
- **[Redis Modules](https://redis.io/modules)** - Módulos oficiais
- **[GitHub](https://github.com/redis/redis)** - Código fonte

### 📖 Documentação Especializada

- **[Redis Sentinel](https://redis.io/topics/sentinel)** - Alta disponibilidade
- **[Redis Cluster](https://redis.io/topics/cluster-tutorial)** - Clustering
- **[Redis Persistence](https://redis.io/topics/persistence)** - RDB e AOF
- **[Redis Security](https://redis.io/topics/security)** - Segurança
- **[Redis Benchmarks](https://redis.io/topics/benchmarks)** - Performance

### 🛠️ Ferramentas Úteis

- **[Redis Desktop Manager](https://resp.app/)** - GUI client
- **[RedisInsight](https://redis.com/redis-enterprise/redis-insight/)** - Ferramenta oficial
- **[redis-cli](https://redis.io/topics/rediscli)** - Cliente de linha de comando
- **[Redis Commander](https://github.com/joeferner/redis-commander)** - Web UI

### 📊 Monitoramento

- **[Redis Exporter](https://github.com/oliver006/redis_exporter)** - Prometheus
- **[Grafana Dashboards](https://grafana.com/grafana/dashboards/?search=redis)** - Dashboards
- **[DataDog Redis](https://docs.datadoghq.com/integrations/redisdb/)** - Integração DataDog
- **[New Relic Redis](https://docs.newrelic.com/docs/infrastructure/host-integrations/host-integrations-list/redis-monitoring-integration/)** - New Relic

### 🎓 Aprendizado

- **[Redis University](https://university.redis.com/)** - Cursos oficiais
- **[Try Redis](https://try.redis.io/)** - Tutorial interativo
- **[Redis Labs](https://redis.com/try-free/)** - Ambiente de teste

### 📚 Livros Recomendados

- **"Redis in Action"** - Josiah Carlson
- **"The Little Redis Book"** - Karl Seguin
- **"Redis Essentials"** - Maxwell Dayvson Da Silva

---

## 🎯 Conclusão

Este guia fornece uma base sólida para instalação, configuração e operação do Redis em ambientes de produção. Redis é uma ferramenta poderosa que, quando configurada corretamente, pode significativamente melhorar a performance de suas aplicações.

### ✅ Próximos Passos

1. **Implementar monitoramento** contínuo
2. **Configurar backup** automatizado
3. **Testar disaster recovery** periodicamente
4. **Otimizar configurações** baseado no uso
5. **Manter Redis atualizado** com patches de segurança

### 🔄 Manutenção Contínua

- **Monitoramento diário** de métricas
- **Backup semanal** com teste de restore
- **Review mensal** de configurações
- **Atualização trimestral** de versões
- **Auditoria anual** de segurança

---
