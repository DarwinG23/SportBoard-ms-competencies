from django.db import models

class Catalogue(models.Model):
    """
    Representa un catálogo jerárquico para clasificaciones generales (ciudades, países, posiciones, etc.).
    Permite relaciones padre-hijo para estructuras anidadas.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Código único del catálogo.")
    description = models.CharField(max_length=255, help_text="Descripción del catálogo.")
    parent_catalog = models.ForeignKey('self', related_name='child_catalogs', null=True, blank=True, on_delete=models.CASCADE, help_text="Catálogo padre (si aplica).")

    def __str__(self):
        return self.description

class User(models.Model):
    """
    Usuario del sistema, asociado a catálogos para ciudad, país, provincia y localización.
    """
    city = models.ForeignKey(Catalogue, related_name='user_city', on_delete=models.PROTECT, help_text="Ciudad del usuario.")
    country = models.ForeignKey(Catalogue, related_name='user_country', on_delete=models.PROTECT, help_text="País del usuario.")
    email = models.EmailField(unique=True, help_text="Correo electrónico único del usuario.")
    first_name = models.CharField(max_length=100, help_text="Nombre del usuario.")
    last_name = models.CharField(max_length=100, help_text="Apellido del usuario.")
    location = models.ForeignKey(Catalogue, related_name='user_location', on_delete=models.PROTECT, help_text="Localización del usuario.")
    is_active = models.BooleanField(default=True, help_text="Indica si el usuario está activo.")
    phone = models.CharField(max_length=20, help_text="Teléfono del usuario.")
    province = models.ForeignKey(Catalogue, related_name='user_province', on_delete=models.PROTECT, help_text="Provincia del usuario.")
    password = models.CharField(max_length=128, help_text="Contraseña cifrada del usuario.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Athlete(models.Model):
    """
    Representa a un atleta, vinculado a un usuario y con atributos deportivos.
    """
    isCoach = models.BooleanField(default=False, help_text="Indica si el atleta es entrenador.")
    isCaptain = models.BooleanField(default=False, help_text="Indica si el atleta es capitán.")
    isActive = models.BooleanField(default=True, help_text="Indica si el atleta está activo.")
    height = models.FloatField(help_text="Altura del atleta en metros.")
    position = models.ForeignKey(Catalogue, related_name='athlete_position', on_delete=models.PROTECT, help_text="Posición del atleta (catálogo).")
    weight = models.FloatField(help_text="Peso del atleta en kilogramos.")
    user = models.OneToOneField(User, related_name='athlete', on_delete=models.CASCADE, help_text="Usuario asociado al atleta.")

    def __str__(self):
        return str(self.user)

class Team(models.Model):
    """
    Representa un equipo deportivo, con nacionalidad y categoría.
    """
    name = models.CharField(max_length=100, help_text="Nombre del equipo.")
    nationality = models.ForeignKey(Catalogue, related_name='team_nationality', on_delete=models.PROTECT, help_text="Nacionalidad del equipo.")
    category = models.ForeignKey('Category', related_name='teams', on_delete=models.SET_NULL, null=True, blank=True, help_text="Categoría del equipo.")

    def __str__(self):
        return self.name

class Administration(models.Model):
    """
    Entidad administrativa responsable de una competencia.
    """
    city = models.ForeignKey(Catalogue, related_name='admin_city', on_delete=models.PROTECT, help_text="Ciudad de la administración.")
    country = models.ForeignKey(Catalogue, related_name='admin_country', on_delete=models.PROTECT, help_text="País de la administración.")
    location = models.ForeignKey(Catalogue, related_name='admin_location', on_delete=models.PROTECT, help_text="Localización de la administración.")
    isActive = models.BooleanField(default=True, help_text="Indica si la administración está activa.")
    name = models.CharField(max_length=100, help_text="Nombre de la administración.")
    phone = models.CharField(max_length=20, help_text="Teléfono de la administración.")
    province = models.ForeignKey(Catalogue, related_name='admin_province', on_delete=models.PROTECT, help_text="Provincia de la administración.")

    def __str__(self):
        return self.name

class GameState(models.Model):
    """
    Estado de un partido (ejemplo: programado, en juego, finalizado).
    """
    description = models.CharField(max_length=255, help_text="Descripción del estado del partido.")
    name = models.CharField(max_length=100, help_text="Nombre del estado del partido.")

    def __str__(self):
        return self.name

class Game(models.Model):
    """
    Representa un partido o juego deportivo.
    """
    endTime = models.DateTimeField(help_text="Fecha y hora de finalización del partido.")
    name = models.CharField(max_length=100, help_text="Nombre del partido.")
    startTime = models.DateTimeField(help_text="Fecha y hora de inicio del partido.")
    gameState = models.ForeignKey(GameState, related_name='games', on_delete=models.PROTECT, help_text="Estado actual del partido.")

    def __str__(self):
        return self.name

class Marker(models.Model):
    """
    Marcador de un partido, almacena los puntos de local y visitante.
    """
    local = models.IntegerField(help_text="Puntos del equipo local.")
    visitor = models.IntegerField(help_text="Puntos del equipo visitante.")
    game = models.ForeignKey(Game, related_name='markers', on_delete=models.CASCADE, help_text="Partido asociado al marcador.")

class Phase(models.Model):
    """
    Fase de una temporada o competencia (ejemplo: grupos, semifinal, final).
    """
    description = models.CharField(max_length=255, help_text="Descripción de la fase.")
    modality = models.ForeignKey(Catalogue, related_name='phase_modality', on_delete=models.PROTECT, help_text="Modalidad de la fase.")
    name = models.CharField(max_length=100, help_text="Nombre de la fase.")
    season = models.ForeignKey('Season', related_name='phases', on_delete=models.CASCADE, help_text="Temporada asociada a la fase.")
    category = models.ForeignKey('Category', related_name='phases', on_delete=models.PROTECT, help_text="Categoría asociada a la fase.")
    isActive = models.BooleanField(default=True, help_text="Indica si la fase está activa.")

    def __str__(self):
        return self.name

class Offer(models.Model):
    """
    Oferta o propuesta dentro de una fase de competencia.
    """
    creationDate = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación de la oferta.")
    description = models.CharField(max_length=255, help_text="Descripción de la oferta.")
    name = models.CharField(max_length=100, help_text="Nombre de la oferta.")
    isStatic = models.BooleanField(default=False, help_text="Indica si la oferta es estática.")
    phase = models.ForeignKey(Phase, related_name='offers', on_delete=models.CASCADE, help_text="Fase asociada a la oferta.")

    def __str__(self):
        return self.name

class Season(models.Model):
    """
    Temporada de una competencia deportiva.
    """
    champion = models.CharField(max_length=100, help_text="Equipo campeón de la temporada.")
    description = models.CharField(max_length=255, help_text="Descripción de la temporada.")
    endTime = models.DateTimeField(help_text="Fecha de finalización de la temporada.")
    hasEnd = models.BooleanField(default=False, help_text="Indica si la temporada ha finalizado.")
    hasChampion = models.BooleanField(default=False, help_text="Indica si la temporada tiene campeón definido.")
    name = models.CharField(max_length=100, help_text="Nombre de la temporada.")
    startDate = models.DateTimeField(help_text="Fecha de inicio de la temporada.")
    subChampion = models.CharField(max_length=100, help_text="Equipo subcampeón de la temporada.")
    competition = models.ForeignKey('Competition', related_name='seasons', on_delete=models.CASCADE, help_text="Competencia asociada a la temporada.")

    def __str__(self):
        return self.name

class Competition(models.Model):
    """
    Competencia deportiva gestionada por la plataforma.
    """
    creationDate = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación de la competencia.")
    name = models.CharField(max_length=100, help_text="Nombre de la competencia.")
    administration = models.ForeignKey(Administration, related_name='competitions', on_delete=models.PROTECT, help_text="Administración responsable de la competencia.")

    def __str__(self):
        return self.name

class Rule(models.Model):
    """
    Reglas asociadas a las categorías y competencias.
    """
    code = models.CharField(max_length=50, unique=True, help_text="Código único de la regla.")
    description = models.CharField(max_length=255, help_text="Descripción de la regla.")
    name = models.CharField(max_length=100, help_text="Nombre de la regla.")

    def __str__(self):
        return self.name

class Category(models.Model):
    """
    Categoría deportiva (ejemplo: sub-18, profesional).
    """
    age_init = models.IntegerField(help_text="Edad mínima de la categoría.")
    age_end = models.IntegerField(help_text="Edad máxima de la categoría.")
    name = models.CharField(max_length=100, help_text="Nombre de la categoría.")
    rule = models.ForeignKey(Rule, related_name='categories', on_delete=models.PROTECT, help_text="Regla asociada a la categoría.")

    def __str__(self):
        return self.name

class PositionTable(models.Model):
    """
    Tabla de posiciones de los equipos en una competencia.
    """
    position = models.IntegerField(help_text="Posición del equipo en la tabla.")
    points = models.IntegerField(help_text="Puntos acumulados por el equipo.")
    team = models.ForeignKey(Team, related_name='position_tables', on_delete=models.CASCADE, help_text="Equipo asociado a la posición.")

class TableRating(models.Model):
    """
    Calificación o rating de la tabla de posiciones.
    """
    lastUpdate = models.DateTimeField(auto_now=True, help_text="Fecha de última actualización del rating.")
    positionTable = models.ForeignKey(PositionTable, related_name='table_ratings', on_delete=models.CASCADE, help_text="Tabla de posiciones asociada.")

    def __str__(self):
        return f"{self.positionTable.team.name} - {self.lastUpdate}"
