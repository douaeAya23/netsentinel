"""Features analysées en EDA, avec leur intérêt pour la détection d'intrusions."""

KEY_FEATURE_DESCRIPTIONS: dict[str, str] = {
    "flow_duration": "Durée du flux (µs) : courte pour un scan, longue pour une attaque lente",
    "total_fwd_packets": "Paquets envoyés par l'émetteur de la connexion",
    "total_backward_packets": "Paquets de réponse : 1 pour un scan, 0 pour Slowhttptest",
    "total_length_of_fwd_packets": "Octets envoyés par l'émetteur",
    "flow_bytes_s": "Débit en octets par seconde",
    "flow_packets_s": "Débit en paquets/s : maximal pour PortScan, très faible pour les DoS",
    "fwd_packets_s": "Paquets envoyés par seconde par l'émetteur",
    "flow_iat_mean": "Délai moyen entre paquets : plusieurs secondes pour les DoS lents",
    "packet_length_mean": "Taille moyenne des paquets",
    "average_packet_size": "Taille moyenne globale des paquets du flux",
    "syn_flag_count": "Drapeaux SYN (ouverture TCP) : médiane nulle sauf pour Infiltration",
    "ack_flag_count": "Drapeaux ACK : reflètent une conversation TCP établie",
    "psh_flag_count": "Drapeaux PSH : envoi immédiat des données applicatives",
    "init_win_bytes_forward": "Fenêtre TCP initiale : signature de l'émetteur, biais possible",
}

KEY_FEATURES: tuple[str, ...] = tuple(KEY_FEATURE_DESCRIPTIONS)