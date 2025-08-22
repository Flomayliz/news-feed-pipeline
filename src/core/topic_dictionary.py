from typing import List
import random

TOPIC_KEYWORDS = {
    "ai": [
        # core & models
        "artificial intelligence",
        "ai",
        "machine learning",
        "deep learning",
        "neural network",
        "neural networks",
        "generative ai",
        "foundation model",
        "foundation models",
        "large language model",
        "large language models",
        "gpt",
        "transformer",
        "transformers",
        "diffusion model",
        "diffusion models",
        "multimodal",
        "vision-language model",
        "vlm",
        # tasks & capabilities
        "text generation",
        "image generation",
        "video generation",
        "speech recognition",
        "speech-to-text",
        "text-to-speech",
        "voice cloning",
        "chatbot",
        "chatbots",
        "recommendation system",
        "recommendation engine",
        # retrieval & semantics
        "retrieval augmented generation",
        "rag",
        "embeddings",
        "vector search",
        "semantic search",
        # training & ops
        "prompt engineering",
        "few-shot",
        "zero-shot",
        "fine-tuning",
        "inference",
        "model serving",
        "mlops",
        "rlhf",
        "self-supervised learning",
        "synthetic data",
        # agents & tooling
        "ai agent",
        "ai agents",
        "tool use",
        "function calling",
        # safety & alignment
        "alignment",
        "safety",
        "guardrails",
        # common model families (helpful in headlines)
        "llama",
        "gemini",
        "claude",
        "gpt-4",
        "gpt-5",
    ],
    "marketing": [
        # core & channels
        "marketing",
        "digital marketing",
        "content marketing",
        "social media marketing",
        "email marketing",
        "influencer marketing",
        "performance marketing",
        "growth marketing",
        "brand marketing",
        "product marketing",
        # ads
        "advertising",
        "online advertising",
        "programmatic advertising",
        "display advertising",
        "search ads",
        "social ads",
        "video ads",
        "native ads",
        "retargeting",
        "remarketing",
        # seo / sem / ppc
        "seo",
        "search engine optimization",
        "sem",
        "search engine marketing",
        "ppc",
        "paid search",
        "google ads",
        # data, automation, crm
        "marketing automation",
        "martech",
        "adtech",
        "crm",
        "customer relationship management",
        "customer data platform",
        "cdp",
        "first-party data",
        "audience segmentation",
        "customer segmentation",
        "personalization",
        "journey orchestration",
        # conversion & experimentation
        "conversion rate",
        "cro",
        "a/b testing",
        "experimentation",
        "attribution",
        "attribution modeling",
        "multi-touch attribution",
        # metrics & economics
        "roas",
        "cac",
        "ltv",
        "ctr",
        "cpc",
        "cpm",
        # lifecycle & demand
        "lead generation",
        "lead gen",
        "demand generation",
        "marketing funnel",
        "omnichannel",
        "lifecycle marketing",
        "retention marketing",
        "loyalty program",
        # analytics & tools (high-signal names)
        "marketing analytics",
        "ga4",
        "google analytics 4",
        "meta ads",
        "facebook ads",
        "instagram ads",
        "tiktok ads",
        "linkedin ads",
        "youtube ads",
        # privacy & compliance
        "third-party cookies",
        "cookie deprecation",
        "consent management",
        "gdpr compliance",
    ],
    "science": [
        "scientific study",
        "peer-reviewed",
        "researchers",
        "scientists",
        "laboratory",
        "lab",
        "experiment",
        "preprint",
        "arxiv",
        "doi",
        "journal article",
        "published in",
        # life sciences
        "biology",
        "molecular biology",
        "cell biology",
        "biochemistry",
        "genetics",
        "genomics",
        "immunology",
        "virology",
        "microbiology",
        "neuroscience",
        "physiology",
        # physical & earth sciences
        "physics",
        "quantum physics",
        "quantum mechanics",
        "optics",
        "chemistry",
        "materials science",
        "nanotechnology",
        "earth science",
        "geology",
        "meteorology",
        "oceanography",
        "environmental science",
        "ecology",
        "climate science",
        "climate change",
        "astronomy",
        "astrophysics",
        "cosmology",
        "paleontology",
    ],
}


def get_topics() -> List[str]:
    """
    Returns a list of all topics.
    """
    return list(TOPIC_KEYWORDS.keys())


def get_keywords(topic: str) -> List[str]:
    """
    Returns a list of keywords for a given topic.
    """
    return TOPIC_KEYWORDS.get(topic, [])


def get_all_keywords() -> List[str]:
    """
    Returns a list of all keywords across all topics.
    """
    keywords = []
    for topic in TOPIC_KEYWORDS.values():
        keywords.extend(topic)

    random.shuffle(keywords)  # Shuffle to avoid bias in keyword order

    return keywords
