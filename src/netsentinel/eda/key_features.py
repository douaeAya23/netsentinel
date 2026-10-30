"""Features analysées en EDA, avec leur intérêt pour la détection d'intrusions."""

KEY_FEATURE_DESCRIPTIONS: dict[str, str] = {
    "flow_duration": "Durée du flux (µs) : les scans sont très courts, les attaques lentes très longs",
    "total_fwd_packets": "Paquets envoyés par l'émetteur de la connexion",
    "total_backward_packets": "Paquets de réponse : un scan en reçoit souvent peu ou pas",
    "total_length_of_fwd_packets": "Octets envoyés par l'émetteur",
    "flow_bytes_s": "Débit en octets par seconde",
    "flow_packets_s": "Débit en paquets par seconde : typiquement élevé lors d'un déni de service",
    "fwd_packets_s": "Paquets envoyés par seconde par l'émetteur",
    "flow_iat_mean": "Délai moyen entre paquets : très régulier pour un script automatisé",
    "packet_length_mean": "Taille moyenne des paquets",
    "average_packet_size": "Taille moyenne globale des paquets du flux",
    "syn_flag_count": "Drapeaux SYN (ouverture de connexion TCP) : au cœur des scans de ports",
    "ack_flag_count": "Drapeaux ACK : reflètent une conversation TCP établie",
    "psh_flag_count": "Drapeaux PSH : envoi immédiat de données, fréquent dans les échanges applicatifs",
    "init_win_bytes_forward": "Fenêtre TCP initiale : dépend de l'outil et du système de l'émetteur",
}

KEY_FEATURES: tuple[str, ...] = tuple(KEY_FEATURE_DESCRIPTIONS)