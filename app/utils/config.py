from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    # listens on the redis channel for messages
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_USER: str = "default"
    REDIS_SSL: bool = False
    REDIS_PASSWORD: str = "sOmE_sEcUrE_pAsS"
    REDIS_DB: int = 1

    # Elasticsearch configuration
    ELASTICSEARCH_HOST: str = "elasticsearch"
    ELASTICSEARCH_PORT: int = "9200"
    # ELASTICSEARCH_USER: str = "default"
    # ELASTICSEARCH_PASSWORD: str = "not used"
    ELASTICSEARCH_INDEX: str = "chatbot2"

    # LLM, i am hosting with vllm locally
    LLM_API_KEY: str = "does not matter"
    # LLM_BASE_URL: str = "http://10.4.33.15:80/v1"
    # LLM_NAME: str = "inarikami/DeepSeek-R1-Distill-Qwen-32B-AWQ"
    LLM_BASE_URL: str = "http://10.4.33.7:80/v1"
    LLM_NAME: str = "Qwen/Qwen2-VL-7B-Instruct-GPTQ-Int4"


env = EnvSettings()

if __name__ == "__main__":
    print(env)
