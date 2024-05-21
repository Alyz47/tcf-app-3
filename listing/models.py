from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from account.models import User, Profile
from core.models import Extensions, TimeStampedModel
import os 


class Category(Extensions):
    MAIN_CAT_CHOICES = [
        ("top", "Top"),
        ("bottom", "Bottom"),
        ("footwear", "Footwear"),
    ]

    name = models.CharField(
        choices=MAIN_CAT_CHOICES,
        verbose_name="Category Name",
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(max_length=100, null=True, blank=True)
    image = models.ImageField(verbose_name="Main Category Cover Image", upload_to="images/", null=True, blank=True)

    class Meta:
        verbose_name = "Main Category"
        verbose_name_plural = "Main Categories"

    def __str__(self):
        return self.slug


def subcat_image_upload_path(instance, filename):
    # Get the filename and extension
    base_filename, file_extension = os.path.splitext(filename)
    # Generate the new filename
    new_filename = f"{instance.main_category}/{base_filename}{file_extension}"
    # Return the upload path
    return os.path.join("categories", new_filename)


class SubCategory(Extensions):
    GENDER_CHOICES = [
        ("men", "Men"),
        ("women", "Women"),
        ("others", "Others")
    ]
    name = models.CharField(verbose_name="Sub-category Name", max_length=155)
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=155, null=True, blank=True)
    image = models.ImageField(verbose_name="Category Cover Image", upload_to=subcat_image_upload_path, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=25, null=True, blank=True)

    class Meta:
        verbose_name = "Sub-category"
        verbose_name_plural = "Sub-categories"

    def __str__(self):
        return f"{self.gender} - {self.main_category} - {self.slug}"


class Size(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    size = models.CharField(max_length=50)

    class Meta:
        unique_together = ('category', 'size')

    def __str__(self):
        return f"{self.category} - {self.size}"


class Listing(Extensions):
    GENDER_CHOICES = [
        ("men", "Men"),
        ("women", "Women"),
    ]

    CONDITION_CHOICES = [
        ("Heavily Used", "Heavily Used"),
        ("Well Used", "Well Used"),
        ("Lightly Used", "Lightly Used"),
        ("Like New", "Like New"),
        ("Brand New", "Brand New"),
    ]

    COLOR_CHOICES = [
        ('White', 'White'),
        ('Black', 'Black'),
        ('Beige', 'Beige'),
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
        ('Orange', 'Orange'),
        ('Purple', 'Purple'),
        ('Pink', 'Pink'),
        ('Brown', 'Brown'),
        ('Grey', 'Grey'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Multi', 'Multi'),
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=25, null=True, blank=True)
    category = models.ForeignKey(SubCategory,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True
                                 )  # Stores extracted category from ML model
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=100)
    color = models.CharField(choices=COLOR_CHOICES, max_length=100)
    is_sold = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"

    def __str__(self):
        return str(self.pk)


class ListingImage(Extensions):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="listing_image"
    )
    image = models.ImageField(
        verbose_name="image",
        upload_to="images/",
        default="images/default.png",
    )
    is_cover = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Listing Image"
        verbose_name_plural = "Listing Images"

    def __str__(self):
        return f"Listing Image -> Listing PK: {self.listing} Image: {self.image}"


class Feedback(Extensions):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return str(self.rating)


class Preference(Extensions):
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        # return f"{str(self.user_profile.user.username)} ---> {self.category} + {self.size}"
        return self.user_profile.user.username


class PreferredSubCategory(TimeStampedModel):
    preference = models.ForeignKey(
        Preference,
        related_name='preferred_subcategories',
        on_delete=models.CASCADE
        )
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Preferred Sub-Category"
        verbose_name_plural = "Preferred Sub-Categories"

    def __str__(self):
        return f"{self.preference} - {self.sub_category}"


class PreferredSize(TimeStampedModel):
    preference = models.ForeignKey(
        Preference,
        related_name='preferred_sizes',
        on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.preference} - {self.size}"


class SubCategoryClassification(Extensions):
    # listing_image = models.ForeignKey(ListingImage, on_delete=models.CASCADE)
    # listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    uploaded_image = models.ImageField(verbose_name="image", upload_to="images/")
    sub_category = models.CharField(max_length=155, default='', null=True, blank=True)
    score = models.DecimalField(decimal_places=5, max_digits=10, null=True, blank=True)

    def __str__(self):
        return f"{self.uploaded_image} -> {self.sub_category}"
