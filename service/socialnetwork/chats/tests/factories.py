from factory.django import DjangoModelFactory
import factory


class ChatRoomFactory(DjangoModelFactory):
    class Meta:
        model = "chats.ChatRoom"

    name = factory.Sequence(lambda n: "chat_{0}".format(n))
    admin = factory.SubFactory("users.tests.factories.UserFactory")

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return
        # Add the iterable of groups using bulk addition
        self.members.set(extracted)
