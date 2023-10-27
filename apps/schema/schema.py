import graphene
from django.utils import timezone
from graphene_django import DjangoObjectType

from apps.users.models import User as UserModel
from apps.decks.models import Deck as DeckModel
from apps.cards.models import Card as CardModel


def return_date_time(days: int):
    now = timezone.now()
    return now + timezone.timedelta(days=days)


class User(DjangoObjectType):
    class Meta:
        model = UserModel


class Deck(DjangoObjectType):
    class Meta:
        model = DeckModel


class Card(DjangoObjectType):
    class Meta:
        model = CardModel


class CreateCardMutaion(graphene.Mutation):
    card = graphene.Field(Card)
    class Arguments:
        deck_id = graphene.ID()
        question = graphene.String()
        answer = graphene.String()
    
    def mutate(self, info, question, answer, deck_id):
        deck = DeckModel.objects.get(id=deck_id)
        card = CardModel(question=question, answer=answer, deck=deck)
        card.save()
        return CreateCardMutaion(card=card)


class UpdateCardMutation(graphene.Mutation):
    card = graphene.Field(Card)
    class Arguments:
        id = graphene.ID()
        deck = graphene.Int()
        questoin = graphene.String()
        answer = graphene.String()
        bucket = graphene.Int()
        next_review_at = graphene.DateTime()


    def mutate(self,
               info,
               id,
               deck,
               question,
               answer,
               bucket,
               next_review_at):
        card: CardModel = CardModel.objects.get(id=id).\
            select_related('deck')
        card.deck = deck
        card.question = question
        card.answer = answer
        card.bucket = bucket
        card.next_review_at = return_date_time(next_review_at)
        card.save()


class CreateDeckMutaion(graphene.Mutation):
    deck = graphene.Field(Deck)
    class Arguments:
        title = graphene.String()
        description = graphene.String()
    
    def mutate(self, info, title, description):
        deck = DeckModel(title=title, description=description)
        deck.save()
        return CreateDeckMutaion(deck=deck)


class UpdateDeckMutation(graphene.Mutation):
    deck = graphene.Field(Deck)
    
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
    
    def mutate(self, info, id, title=None, description=None):
        try:
            deck = DeckModel.objects.get(id=id)
        except DeckModel.DoesNotExist as e:
            raise e
        if title:
            deck.title = title
        if description:
            deck.description = description
        deck.save()
        return UpdateDeckMutation(deck=deck)

class Mutation(graphene.ObjectType):
    create_card = CreateCardMutaion.Field()
    create_deck = CreateDeckMutaion.Field()
    update_deck = UpdateDeckMutation.Field()   


class Query(graphene.ObjectType):
    users = graphene.List(User)
    decks = graphene.List(Deck)
    deck_by_id = graphene.Field(Deck, id=graphene.Int())
    cards = graphene.List(Card)
    card_by_id = graphene.Field(Card, id=graphene.Int())
    deck_cards = graphene.List(Card, deck=graphene.Int())

    def resolve_users(self, info, **kwargs):
        return UserModel.objects.all()
    
    def resolve_decks(self, info, **kwargs):
        return DeckModel.objects.all()
    
    def resolve_deck_by_id(self, info, id, **kwargs):
        return DeckModel.objects.get(id=id)
    
    def resolve_deck_cards(self, info, deck, **kwargs):
        return CardModel.objects.filter(deck=deck)
    
    def resolve_cards(self, info, **kwargs):
        return CardModel.objects.all()
    
    def resolve_card_by_id(self, info, id):
        return CardModel.objects.get(id=id)


schema = graphene.Schema(query=Query, mutation=Mutation)