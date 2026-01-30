import re
from typing import Tuple

class EmailValidator:
    """
    Utilitário para validação adicional de emails.
    Complementa a validação do Pydantic (EmailStr).
    """
    
    # Padrão regex para validação mais rigorosa de email
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Lista de domínios descartáveis (opcional)
    DISPOSABLE_DOMAINS = {
        'tempmail.com',
        'guerrillamail.com',
        '10minutemail.com',
        'throwaway.email',
        'mailinator.com',
    }
    
    @staticmethod
    def is_valid_format(email: str) -> Tuple[bool, str]:
        """
        Valida o formato do email usando regex.
        
        Returns:
            Tuple[bool, str]: (é válido, mensagem de erro)
        """
        if not email or len(email) > 254:
            return False, "Email inválido: vazio ou muito longo"
        
        if not re.match(EmailValidator.EMAIL_PATTERN, email):
            return False, "Email inválido: formato incorreto"
        
        return True, ""
    
    @staticmethod
    def is_disposable(email: str) -> Tuple[bool, str]:
        """
        Verifica se o email é de um domínio descartável.
        
        Returns:
            Tuple[bool, str]: (é descartável, mensagem)
        """
        domain = email.split('@')[1].lower()
        
        if domain in EmailValidator.DISPOSABLE_DOMAINS:
            return True, f"Email de domínio descartável não permitido: {domain}"
        
        return False, ""
    
    @staticmethod
    def validate_email(email: str, check_disposable: bool = False) -> Tuple[bool, str]:
        """
        Realiza validação completa do email.
        
        Args:
            email: Email a validar
            check_disposable: Se True, valida também contra domínios descartáveis
        
        Returns:
            Tuple[bool, str]: (é válido, mensagem de erro se houver)
        """
        # Validar formato
        is_valid, error_msg = EmailValidator.is_valid_format(email)
        if not is_valid:
            return False, error_msg
        
        # Validar domínios descartáveis (opcional)
        if check_disposable:
            is_disposable, error_msg = EmailValidator.is_disposable(email)
            if is_disposable:
                return False, error_msg
        
        return True, ""
